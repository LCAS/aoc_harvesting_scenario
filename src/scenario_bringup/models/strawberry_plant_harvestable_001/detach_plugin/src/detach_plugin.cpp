#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>
#include <iostream>
#include <iomanip>
#include <unordered_set>

#include <gazebo/sensors/sensors.hh>
#include <gazebo/sensors/ForceTorqueSensor.hh>
#include <gazebo/transport/transport.hh>

namespace gazebo
{
  class NormalPlugin : public ModelPlugin
  {
  public:

    // Effort values and frequency
    double normalStressThreshold = 1.5;
    double shearStressThreshold = 0.7;
    double readInterval = 0.01;

    void Load(physics::ModelPtr _model, sdf::ElementPtr /*_sdf*/) override
    {
      this->model = _model;

      std::string jointName = "1l15_fruit1";
      this->joint = this->model->GetJoint(jointName);
      this->lastPrintTime = this->model->GetWorld()->SimTime();

      if (!this->joint)
      {
        gzerr << "Joint not found: " << jointName << std::endl;
      }
      for (int i = 1; i <= 15; ++i)
      {
        std::string linkName = "1l" + std::to_string(i);
        auto link = this->model->GetLink(linkName);
        if (!link)
        {
          gzerr << "Link not found: " << linkName << std::endl;
        }
        else
        {
          this->links[i] = link;
        }

        if (i < 15)
        {
          std::string jointName = "1l" + std::to_string(i) + "_" + std::to_string(i + 1);
          auto joint = this->model->GetJoint(jointName);
          if (!joint)
          {
            gzerr << "Joint not found: " << jointName << std::endl;
          }
          else
          {
            this->joints[i] = joint;
          }
        }
      }

      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&NormalPlugin::OnUpdate, this));
    }

    void OnUpdate()
    {
      common::Time currentTime = this->model->GetWorld()->SimTime();

      if ((currentTime - this->lastPrintTime).Double() >= this->readInterval)
      {

        if (this->joint)
        {
          if (!this->sensor)
          {
            auto sensorPtr = sensors::SensorManager::Instance()->GetSensor("joint_force_sensor");
            this->sensor = std::dynamic_pointer_cast<sensors::ForceTorqueSensor>(sensorPtr);
            if (!this->sensor)
              return;
          }

          ignition::math::Vector3d forces = this->sensor->Force();
          double magnitud = forces.Length();

          std::cout << "[JOINT] Stb: "
                    << std::fixed << std::setprecision(7) << std::setw(10) << magnitud
                    << " | "
                    << std::setw(10) << forces
                    << std::endl;

          if (magnitud > this->normalStressThreshold)
          {
            std::cout << "[Plugin] Normal stress exceeded. Joint decoupling.\n";
            this->joint->Detach();
          }
        }

        for (int i = 1; i <= 14; ++i)
        {
          if (this->links.count(i) == 0 || this->joints.count(i) == 0)
            continue;

          auto link = this->links[i];
          auto joint = this->joints[i];

          if (this->desacoplados.count(i))
            continue;

          ignition::math::Vector3d force = link->WorldForce();
          double magnitude = force.Length();

          if (magnitude > this->shearStressThreshold)
          {
            std::cout << "[Plugin] Shear force exceeded in link 1l" << i
                      << ". Uncoupling joint 1l" << i << "_" << i + 1 << std::endl;

            joint->Detach();

            for (auto col : link->GetCollisions())
            {
              col->SetCollideBits(0x00);
              col->SetCategoryBits(0x00);
            }

            this->desacoplados.insert(i);
          }
        }

        this->lastPrintTime = currentTime;
      }
    }

  private:
    physics::ModelPtr model;
    physics::JointPtr joint;
    event::ConnectionPtr updateConnection;
    common::Time lastPrintTime;
    sensors::ForceTorqueSensorPtr sensor;

    std::map<int, physics::LinkPtr> links;
    std::map<int, physics::JointPtr> joints;
    std::unordered_set<int> desacoplados;
  };

  GZ_REGISTER_MODEL_PLUGIN(NormalPlugin)
}
