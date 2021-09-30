# PIOSerialPlotter

### No Serial Plotter for PlatformIO/VSCode ???

<p>The following picture is the Arduino IDE's serial plotter, but the PlatformIO and/or VSCode don't have it. Hence it's made and this repo is the equivalent to that.</p>

![Arduino Serial Plotter](https://user-images.githubusercontent.com/13171662/133396210-a3c486cc-1c94-4cdc-abd9-7f56042f0f2f.png)


<p>This tool can be run stand alone with the usage below. This needs to be started in the PIO Terminal Panel, specifically in the PIO bundled python venv.</p>
<pre>
Usage:

         python /Users/yhur/.platformio/packages/tool-serialplotter/serialPlotter.py [-h] [-w 100] [-t ChartTitle] [-s 5050] [dataLabel1] [dataLabel2 ...]]

                OR

         python /Users/yhur/.platformio/packages/tool-serialplotter/serialPlotter.py [--help] [--width=100] [--title=ChartTitle] [--socket=5050] [dataLabel1] [dataLabel2 ...]
</pre>
<ul>
  <li>-h | --help : This option prints the above usage.</li>
<li>-t | --titile : This let you change the title of the page.</li>
<li>-w | --width : This let you adjust the plot X axis and the number of data spots. The default is 50.</li>
<li>-s | --socket : This tool can listen on a TCP port and plot the data instead of the serial port if this TCP port number is provided.</li>
</ul>
As an example, when you run it this way,
<pre>
pytho PlotSerialData.py -t Thermometer -w 100 Temperature Humidity
</pre>
You'll see see the plot like this
<img width="888" alt="Screen Shot 2021-09-15 at 5 06 58 PM" src="https://user-images.githubusercontent.com/13171662/133395207-5af9da40-59a1-48e0-995d-72a0bf3d386e.png">

### Optional Plot Configuration
There is an optional configuration file where you can set the setting for the plotting for the project. When you create a json file named **'plotcfg.json'** under the root directory of the PIO project, you don't have to pass the setting every time you invoke the tool.
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
## Prerequisite
* This plotter uses the matplotlib, so you need to install it by this command.
<pre>
pip install matplotlib
</pre>
* Download and place the python code where you can easily recall and call.

