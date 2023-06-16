# Smart Toled Glasses With Word Translation

If you have been with me in the previous project with the Smart Glasses then we are not done yet!
If not it's fine, don't worry!

We want to receive information from the internet about the Weather and Currency and with Artificial Neural Networking (ANN)  we want to translate English words to Turkish words.
The Currency and Weather information will be taken from internet directly with the Raspberry Pi 3B+, however for the word translation, we will take a photo from the Raspberry Pi 3B+ from the camera mounted on it and send it through the internet to the main computer where the main computer will itself translate then send back the information to the Raspberry Pi 3B+. 
The information will be projected to the transparent glasses. The idea of this project is to be able to display information to the user directly in front of his/her eyes without losing sight of what is in the horizon and without having to move a single movement except only to change tabs between different information.


![Planning](https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/2302ab5a-2aa8-4ab0-9404-17d12ba9bbf8)

So for this project we will only do for 50 Words with ANN with 720 training data for each word because it takes a lot of processing power (and consequently time) but hey if you have the processing power for more, then you can edit it to suit your needs.
Our 50 Words are:
 
|    All    |   Less  |  Sell  |
|:---------:|:-------:|:------:|
|   Always  |  Listen |  Short | 
|   Animal  |   Long  | Silver |
|   Book    |   Many  |   Sit  |
|   Buy     |   Month |  Smile |
|   Car     |   Name  |  Sorry |
|   Chair   |   Never |  Speak |
|   Child   |   New   |  Study |
|   City    |   Noise |  Table | 
|Day
|Drink
|Family
|Food
|Friend
|Home
|Inside
|Laugh

<div style="display: flex;">
  <table>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
      <th>Header 3</th>
    </tr>
    <tr>
      <td>Cell 1</td>
      <td>Cell 2</td>
      <td>Cell 3</td>
    </tr>
    <tr>
      <td>Cell 4</td>
      <td>Cell 5</td>
      <td>Cell 6</td>
    </tr>
  </table>

  <div style="margin-left: 20px;">
    This is some text that appears to the right of the table.
  </div>
</div>
