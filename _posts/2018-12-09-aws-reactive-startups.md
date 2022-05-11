---
author: ianfhunter
category: 1 technical
date: 9 Dec 2018
description: Save money by turning machines off when they're not being used
math: true
mermaid: true
share: true
tag:
- writing
---

# Reactive Startup for Jenkins on AWS

## Motive

AWS machines are deceptively expensive. Included below are a list of general use machine prices on Amazon’s storefront. 50 cent for one hour doesn’t seem so bad - but what if you have it up 24/7 ? The costs accrue quickly and one server could set you back $416 with only a month’s use.

<img src='/assets/img/notes/Price_Tiers.png' />

Imagine a large-scale business. It uses AWS machines throughout many places in the deployment to Live process - Service Testing, Integration Testing, Pre-Production, etc. Along with this we have several teams, each with their own requirements - may that be load testing, distributed deployment or something else. A business like such will require many machines with varying costs.

First in line to cut costs is to only allocate machines to those that really need them, and to use the sizes they need - You don’t need a heavy duty box to run some lightweight database tests. To further enhance cost reduction, you can also set up dynamic starting/stopping of your machines.

## Operation

A development server runs Jenkins and runs through a set of build and testing scripts every time a push to version control happens. This setup might be a simple single-machines setup, or it may involve several machines, with similar or different purposes.

<img src='/assets/img/notes/Master_Slave_Setup.png' />

First, the main Jenkins process and the agent processes must be configured to restart on startup. This should ideally be done regardless of whether you continue with this method or not in order to recover your Jenkins instance faster after reboot. This will involve a fairly easy process with Windows through the built-in Task Scheduler or by adding some scripts within /etc/init.d/ on Gnu/Linux.

<img src='/assets/img/notes/Task_Scheduler_Screenshot.png' />

You may need to configure other processes/services for startup depending on your setup. Now the servers are prepared for accidental shutdowns. Or purposeful ones, which is what the next step entails.

![[On-Off.png]]

We set up two Jenkins jobs: One to monitor for activity, another to monitor for inactivity. Every 20 minutes or so, we check if there are any jobs currently running with Jenkins, and if there are any jobs run in the last hour. If not, we shutdown the agent machines using the AWS Powershell Tools (a simple call like Stop-EC2Instance machine.domain.com ). After a while without any jobs running, the machine will shutdown Similarly the other job checks every 4 minutes for pending jobs, as any jobs triggered while no machines are available will stall until they can execute. Jobs are triggered on Jenkins. At the next check, machines are made available and the jobs can progress We check the jobs’ statuses through our Jenkin’s Remote Access API through a small Python script.

<img src='/assets/img/notes/Zoomed_Out.png' />

## Result

Of course, starting machines before a job run will increase the runtime for that job, but this process only adds about 2 or so minutes to the process. After this initial slowdown, machines are active for the next hour or longer, assuming that the successive jobs will be temporarily located. There is a caveat to be careful of when using the AWS Tools - if you boot twice within the hour, it counts as two hours of usage. This is why 1 hour is the recommended back-off time. If we activated this for only non-peak times, we have reduced usage by 66%, essentially reducing a machine like the one mentioned in the intro paragraph from $416 to $138. I imagine this could be reduced to under the $100 mark, but depending on the setup and the amount of activity on your Jenkins this will be more varied month on month.