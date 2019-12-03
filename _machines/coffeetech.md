---
layout: single
permalink: /machines/coffeetech/
title: "Coffee Tech"
excerpt: "FZ-94/Ghibli/Silon"
header:
  overlay_image: /assets/images/ghibli15.jpg
  image: /assets/images/FZ94-1.jpg
  teaser: assets/images/FZ94-1.jpg
---
* __Producer:__ [Coffee-Tech Engineering Ltd.](https://www.coffee-tech.com), Israel
* __Machine:__ FZ-94 Lab Roaster, Ghibli 15/30/45/60/90, and Ghibli Firewood, Silon ZR7
* __Connection:__ 
   * FZ-94/Ghibli: MODBUS RTU via USB-2-RS485 interface; requires the installation of a serial driver
   * Silon ZR7 (touch): MODBUS TCP via network connection
* __Features:__ logging of environmental temperature (ET), bean temperature (BT), drum temperature (DT), set value (SV), fan speed and drum speed. 

### Notes

- the Ghibli series machines do not feature an environmental temperature sensor and report the drum temperature on the Artisan ET channel.
- the setup defines 2 configurations that can be switched via the command key plus a number key.
  * CMD-1 (default): logs drum- and fan speed changes as custom events
  * CMD-2: defines drum- and fan speed sliders that allow to take control via a [re-configuration of the frequency drives](https://artisan-roasterscope.blogspot.de/2016/08/fz-94-4-taking-control.html)
- The drum heat limit can also be controlled via an SV slider by ticking `Control` in the device setup (menu `Config` >> `Device`)