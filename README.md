# Honors Project Description
The project will consist of building software for the nEXO project at SLAC in collaboration with Skyline College. I will be working with Professor Wamba to build software that can aid in the alignment of a laser beam and an optical fiber cable. This is otherwise known as beam steering. The laser light is used to generate electrons that drift in liquid xenon in order to determine the xenon’s chemical purity. The best way to build this software will be what I am researching. Typically, the laser is aligned with two people collaborating in two different rooms. One is looking at an oscilloscope yelling at the other person in the other room, telling the second person how to adjust the laser beam alignment knobs so that the beam is reasonably aligned with the optical fiber cable. The hope is that the completed software will allow the person in the room with the knobs to work independently by providing a visual for them on how well aligned the laser beam is.

This project relates to the computer science and physics fields. We will be building this software in Python. The only requirement for this project is to attempt to complete a draft of the proposed software by the end of the semester. More information about the nEXO project which this honors project is under can be found at https://nexo.llnl.gov/ .

# How to use the Fiber Alignment Tool
1. The tool is located in [scopeclient.py](/scopeclient.py) file therefore download the file.
2. You may need to change the address of where the client connects to the server. Therefore, if needed change the following lines to the proper address but keep with the same commands.
```python
f = urllib.request.urlopen('http://localhost:5022/?COMMAND=curve?')
f2 = urllib.request.urlopen('http://localhost:5022/?COMMAND=wfmpre?')
```
3. With the proper addresses, you can now run the code in your terminal with the following command:
```
python3 scopeclient.py
```
# Fiber Alignment Tool
- The tool should output a GUI similar to the one below:
<!-- ![Example GUI](/example_GUI.png) -->
<img src="/example_GUI.png" width="500" height="300">

- The top graph is a history of the waveform upstroke/peak size.
  - **Waveform upstroke/peak** size is determined by creating a subset of the waveform consisting of values from the 50th value to the value located at the halfway point of the waveform. 
  - We then find the max value of this subset giving us the highest point in the upstroke.
  - We then check the previous 50 points starting from the highest point in the upstroke to find where the upstroke begins.
  - With the max and min value of the upstroke, we subtract the min from the max to obtain our upstroke/peak size 
  - This process is shown in the code below:
```python
volt_subset = volt[50:int(len(volt) / 2)]
max_index = np.argmax(volt_subset)

peak = volt_subset[max_index] - np.min(volt_subset[max_index-50:max_index])
```
- The bottom graph depicts the most recent waveform.

# Future Directions
- The current [scopeclient.py](/scopeclient.py) is not built to handle special cases such as a null waveform or a waveform consistently mostly of zeroes. This most likely causes issues in plotting. Working around this or building a case to handle will make the code more robust.  
- The way in which the peak is calculated can also be improved as our program assumes the highest value of the upstroke does not happen within the first 50 values of the waveform. Using derivatives or another technqiue may be more efficient. 
