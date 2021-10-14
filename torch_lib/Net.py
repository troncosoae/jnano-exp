from tensorflow.python.util.nest import flatten
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.model_list = [
            nn.Conv2d(
                3, out_channels=6, kernel_size=5, padding=0),
            F.relu,
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(
                6, out_channels=16, kernel_size=5, padding=0),
            F.relu,
            nn.MaxPool2d(kernel_size=2, stride=2),
            lambda x: torch.flatten(x, 1),
            nn.Linear(16*5*5, 120),
            F.relu,
            nn.Linear(120, 84),
            F.relu,
            nn.Linear(84, 10)
        ]

    def forward(self, x):
        for f in self.model_list:
            x = f(x)
        return x

    def train(self, dataset_batches, epochs, verbose=False, **kwargs):
        criterion = kwargs.get('criterion', nn.CrossEntropyLoss())
        optimizer = kwargs.get('optimizer', optim.SGD(
            self.parameters(),
            lr=kwargs.get('lr', 0.001),
            momentum=kwargs.get('momentum', 0.9)
            ))

        i = 0
        for epoch in range(epochs):
            running_loss = 0.0
            if verbose:
                print('epoch:', epoch)
            for batch in dataset_batches:
                X, Y = batch
                optimizer.zero_grad()
                Y_pred = self(X)
                # print(Y_pred, Y)
                loss = criterion(Y_pred, Y)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                if i % 2000 == 1999:    # print every 2000 mini-batches
                    print('[%d, %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 2000))
                    running_loss = 0.0
                i += 1
            # print(f'running loss {running_loss:.3f}')

    def save_weights(self, path):
        torch.save(self.state_dict(), path)

    def load_weights(self, path):
        self.load_state_dict(torch.load(path))

    def evaluate_accuracy(self, x, y):
        y_pred = self(x).detach().numpy()
        y_pred = np.argmax(y_pred, axis=1)

        N = y.shape[0]
        correct = 0
        for i in range(N):
            if y_pred[i] == y[i]:
                correct += 1

        return correct/N, N
