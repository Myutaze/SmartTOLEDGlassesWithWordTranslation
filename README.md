# Smart Toled Glasses With Word Translation

If you have been with me in the previous project with the Smart Glasses then we are not done yet!
If not it's fine, don't worry!

We want to receive information from the internet about the Weather and Currency and with Artificial Neural Networking (ANN)  we want to translate English words to Turkish words.
The Currency and Weather information will be taken from internet directly with the Raspberry Pi 3B+, however for the word translation, we will take a photo from the Raspberry Pi 3B+ from the camera mounted on it and send it through the internet to the main computer where the main computer will itself translate then send back the information to the Raspberry Pi 3B+. 
The information will be projected to the transparent glasses. The idea of this project is to be able to display information to the user directly in front of his/her eyes without losing sight of what is in the horizon and without having to move a single movement except only to change tabs between different information.

![Planning](https://github.com/Myutaze/SmartTOLEDGlassesWithWordTranslation/assets/123553691/c90582ba-e0c7-4935-9a03-fbef48d43306)


So for this project we will only do for 50 Words with ANN with 720 training data for each word (36000 for 50 Words) because it takes a lot of processing power (and consequently time) but hey if you have the processing power for more, then you can edit it to suit your needs.
Our 50 Words are:
 

| All     | Less     | Sell     |
|:-------:|:--------:|:--------:|
| Always  | Listen   | Short    |
| Animal  | Long     | Silver   |
| Book    | Many     | Sit      |
| Buy     | Month    | Smile    |
| Car     | Name     | Sorry    |
| Chair   | Never    | Speak    |
| Child   | New      | Study    |
| City    | Noise    | Table    |
| Day     | Often    | Think    |
| Drink   | Old      | Time     |
| Family  | Other    | Walk     |
| Food    | Outside  | Water    |
| Friend  | Pencil   | Work     |
| Home    | People   | Write    |
| Inside  | Power    | Year     |
| Laugh   | School   |          |

