# arduplot

### No Serial Plotter for PlatformIO/VSCode ???

<p>The following picture shows the Arduino IDE's serial plotter which plots the date coming through the serial port.</p>

![Arduino Serial Plotter](https://user-images.githubusercontent.com/13171662/133396210-a3c486cc-1c94-4cdc-abd9-7f56042f0f2f.png)


<p>But there is no built-in equivalent tool for the PlatformIO and/or VSCode. Hence arduplot(Arduino Plot) is made to support the equivalent funcitionality.</p>
<p>This tool can be run stand alone with the usage below. This needs to be started in the PIO Terminal Panel, specifically in the PIO bundled python venv.</p>
<pre>
Usage: arduplot [OPTIONS] [LABELS]...

Options:
  -w, --width INTEGER   Plotter Width
  -t, --title TEXT      Plotter Title
  -s, --socket INTEGER  TCP Socket Port number
  -p, --port TEXT       Serial Port, a number or a device name
  -b, --baud INTEGER    Set baudrate, default=115200
  --help                Show this message and exit.
</pre>
As an example, you can build and run https://github.com/iotlab101/dht22_platformio on an esp8266 and run the following command.
<pre>
arduplot -t Thermometer -w 100 Temperature Humidity
</pre>
Here -t Thermometer is the title of the plot chart, -w 100 is the width of the plot, and Temperature and the Humidity are the labels of the plotting data.
And you'll see see the plot like this


![Screen Shot 2021-11-13 at 9 59 48 PM](https://user-images.githubusercontent.com/13171662/141644699-778221fe-7eb4-4760-bc6b-3f3671e2724d.png)


### Optional Plot Configuration
There is an optional configuration file where you can set the setting for the plotting for the project. If you create a json file named **'plotcfg.json'** under the the PIO project directory, you don't have to pass the parameters every time you invoke the tool.
<pre>
{
    "label": [
        "temperature",
        "humidity"
    ],
    "title": "Thermmeter",
    "width": 100
}
</pre>
This configuration would be helpful, if you want to run this tool over the TCP port via some other tool where it's not easy to pass-through the setting information.
## Installation and Prerequisite
* This plotter uses the following dependancies, and they will be installed when you install this tool..
<pre>
         matplotlib
         click
         pyserial
</pre>
You can install this tool with the pip as follows
<pre>
pip install arduplot
</pre>

## Running it as part of PlatformIO monitor filter ##
1. Install the arduplot first<pre>ip install arduplot</pre>
2. copy ~/.platformio/penv/lib/python3.9/site-packages/arduplot/filter_plotter.py to either 
<pre>
(project_dir)/monitor, 
</pre> 
for every project, or 
<pre>
~/.platformio/platform/espressif8266/monitor (or ~/.platformio/platform/espressif32/monitor for esp32)
</pre>
Or you can just set the environment variable as below and run this without copying.
<pre>
export PLATFORMIO_MONITOR_DIR=$(HOME)/.platformio/penv/lib/python3.9/site-packages/arduplot/
</pre>
3. run pio device monitor -f plotter after installation of the arduplot. And you will get this plot.

<img width="937" alt="Screen Shot 2021-11-13 at 9 46 49 PM" src="https://user-images.githubusercontent.com/13171662/141644389-00e05586-837c-4bd9-9c73-5f61e2785ead.png">

