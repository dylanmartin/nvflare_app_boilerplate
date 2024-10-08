This repository is meant to provide boilerplate code and a basic guide to get started using NVFLARE to make federated computations for COINTSAC.

- [Hello World Tutorial](./tutorial_hello_world.md)
- [Computation Development Notes](./computation_development.md)


# What is NVFLARE?

- NVFLARE is an open-source federated learning tool developed by NVIDIA.

- You can find NVIDIA's documentation and source code here:

  - https://nvflare.readthedocs.io/en/2.4.0/index.html
  - https://github.com/NVIDIA/NVFlare

# Using NVFLARE to develop computations

## Overview

- An NVFLARE Application is the specific computation or learning model you develop. It encapsulates the custom logic and algorithms necessary for your federated learning computation. See the `app/` folder in this repository.

- NVFLARE provides tools for you to develop and test your application:

  - NVFLARE Simulator
  - NVFLARE POC mode

- These tools automate the following steps to running a federated computation:

  - Provisioning: Provisioning a project creates startup kits for various components (sites, server, and admin) necessary for your federated network.
  - Deployment: Launching and connecting the server, sites, and admin components using scripts provided in the startup kits.
  - Execution: Submitting a job that runs your custom app across the federated network.

- Try running the app in Simulator and POC mode, then try modifying the app code.
- Use the following programming guide for developing your own app:
  - https://nvflare.readthedocs.io/en/2.4.0/programming_guide.html

## Developing in a container

- You can choose to develop inside a container or on your local host system.
- If you choose to develop in a container you can use the following command to build a dev docker image

```
docker build -t nvflare-pt -f Dockerfile-dev .
```

- You can launch the container by running `./dockerRun.sh`
- If you're using windows, launch the container by using the following command:

```
docker run --rm -it ^
    --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 ^
    --name flare ^
    -v %cd%:/workspace ^
    -w //workspace ^
    nvflare-pt:latest

```

## Developing on local machine

Install the nvflare package:

```
python3 -m pip install nvflare==2.4.0
```

Make sure the following environment variables are set:

```
export PYTHONPATH=$PYTHONPATH:[path to this dir + ./app/code/]
export NVFLARE_POC_WORKSPACE=[path to this dir + ./poc-workspace/]
```

## NVFLARE Simulator

- The FL Simulator is a lightweight simulator of a running NVFLARE FL deployment, and it can allow researchers to test and debug their application without provisioning a real project.
- https://nvflare.readthedocs.io/en/2.4.0/user_guide/nvflare_cli/fl_simulator.html

### Using NVFLARE Simulator

The simulator can run the entire project as a single thread. This can be useful for attaching a debugger.

The following commands allow you to run the app using the Simulator

```
nvflare simulator -c site1,site2 ./jobs/job
```

## Proof of Concept (POC) Mode

- The POC command allows users to try out the features of NVFlare in a proof of concept deployment on a single machine.
- https://nvflare.readthedocs.io/en/2.4.0/user_guide/nvflare_cli/poc_command.html

### Using POC mode

The following commands allow you to run the app in POC mode

```
nvflare poc prepare -i project.yaml
nvflare poc prepare-jobs-dir -j jobs
nvflare poc start
```

Once the previous command completes your command line will be in the admin shell. From there you can submit your job with the following command:

```
submit_job job
```
