# Zombie Outbreak in American!

## About this script

Code adapted from [Zulko](https://gist.github.com/Zulko/6aa898d22e74aa9dafc3)'s simualtion on the outbreak of zombies in France with the model modified. My original idea was to simulate what would happen in China (because I'm Chinese) but I can not find any satisfactory images of Chinese population density map, so I used American's instead. The background image was downloaded from [NASA's website](https://www.nasa.gov/sites/default/files/images/712129main_8247975848_88635d38a1_o.jpg).

## Dependency

This script relies on ```numpy``` and ```moviepy``` modules.

## About the Model

The basic idea is, one can use a triple ```(S,I,R)``` to represent the densities of the three kinds of "people":
- ```S```: sane people
- ```I```: infected people. They will incubate to zombies.
- ```R```: zombies.

```S,I,R``` are all within [0,1]. 

The advantage of this representation is that the ```(S,I,R)``` triple can also be viewed as a RGB triple so that one can transform the density matrices into RGB images very easily.


