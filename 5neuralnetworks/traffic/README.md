I wanted to experiment with a functional model as opposed to a sequential so I began by implementing that.

For the original functional model I received this as results: 333/333 - 1s - 2ms/step - accuracy: 0.9364 - loss: 0.3778
Not too bad but not great either, this was done wiht a simple structure consisting of 1 1 convolutional , 1 pool and 1 dense dropout layer.

I went on to test the functional model with a bunch more convolutional layers. This time I added 2 more convolutional layers each with a filter vlaue of 64 (opposed to 32 the first time), I also added another pool and 2 more dropout layers. This approach gave me worse results :(. I ran it twice and got the following:

- 333/333 - 1s - 2ms/step - accuracy: 0.9278 - loss: 0.4537
- 333/333 - 1s - 2ms/step - accuracy: 0.9348 - loss: 0.3908
  So within the same ballpark but still noticeably worse then the latter.

I now want to adjust the dropouts and filters to see if we can achieve better results. This time I changed all dropout rates to .1 and changes the filters to 32 and a 3x3 kernel.
On the first run with this I got - 333/333 - 1s - 3ms/step - accuracy: 0.9217 - loss: 0.5559
On the next run I got - 333/333 - 1s - 3ms/step - accuracy: 0.9396 - loss: 0.401
So oddly enough we got the lowest and the highest accuracy rates in this trial. Just shows how comparable all of these models are.

Next I converted the functional model into a sequential model. From the harvard lecture and other information I have seen about similar projects, sequential models are what I see being used. And from my testing I can see why.
First run we got - 333/333 - 1s - 3ms/step - accuracy: 0.9669 - loss: 0.2069
Second we got - 333/333 - 1s - 4ms/step - accuracy: 0.9685 - loss: 0.1566
So the accuracy with the sequential model is clearly much better then the functional model in this case.
