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
As an example, when you run it this way,
<pre>
arduplot -t Thermometer -w 100 Temperature Humidity
</pre>
Here -t Thermometer is the title of the plot chart, -w 100 is the width of the plot, and Temperature and the Humidity are the labels of the plotting date.
And you'll see see the plot like this
<img width="888" alt="Screen Shot 2021-09-15 at 5 06 58 PM" src="https://user-images.githubusercontent.com/13171662/133395207-5af9da40-59a1-48e0-995d-72a0bf3d386e.png">

### Optional Plot Configuration
There is an optional configuration file where you can set the setting for the plotting for the project. If you create a json file named **'plotcfg.json'** under the root directory of the PIO project, you don't have to pass the parameters every time you invoke the tool.
<pre>
{
    "label": [
        "temperature",
        "humidity",
        "hum2"
    ],
    "title": "test",
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


