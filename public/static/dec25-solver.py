from typing import List

import numpy
import pandas as pd
import torch
import torch.nn.functional as F
from torch import nn, optim, Tensor
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataset import T_co
from torch.utils.tensorboard import SummaryWriter

best_vloss = 10000


class HackventDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index) -> T_co:
        if torch.is_tensor(index):
            index = index.tolist()

        return (self.data.iloc[index, 0].astype(float), self.data.iloc[index, 1].astype(float))


training_set = HackventDataset("./data_training.csv")
validation_set = HackventDataset("./data_validation.csv")

training_loader = DataLoader(training_set, batch_size=4, shuffle=True)
validation_loader = DataLoader(validation_set, batch_size=4, shuffle=True)

data_training = numpy.loadtxt("./data_training.csv", delimiter=',')
x_training = data_training[:, 0]
y_training = data_training[:, 1]

y_training: Tensor = torch.from_numpy(y_training.reshape((2000, 1))).float()
x_training: Tensor = torch.from_numpy(x_training.reshape((2000, 1))).float()

data_validation = numpy.loadtxt("./data_validation.csv", delimiter=',')
x_validation = data_validation[:, 0]
y_validation = data_validation[:, 1]

y_validation: Tensor = torch.from_numpy(y_validation.reshape((1000, 1))).float()
x_validation: Tensor = torch.from_numpy(x_validation.reshape((1000, 1))).float()


class HackventModule(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(in_features=1, out_features=1, bias=False)

    def forward(self, x: Tensor):
        x = F.relu(self.linear(x))
        return x


m = HackventModule()

loss_fn = nn.CrossEntropyLoss()

optimizer = optim.SGD(m.parameters(), lr=0.001, momentum=0.9)


def train_one_epoch(epoch_index, tb_writer):
    running_loss = 0
    last_loss = 0

    for i in range(0, len(data_training)):
        input, labels = x_training[i], y_training[i]

        optimizer.zero_grad()
        outputs = m(input)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if i % 1000 == 999:
            last_loss = running_loss / 1000
            tb_x = epoch_index * len(data_training) + i + 1
            tb_writer.add_scalar("Loss/train", last_loss, tb_x)
            running_loss = 0
    return last_loss


writer = SummaryWriter("runs/fashion_trainer")
for epoch in range(5):
    print(f"EPOCH {epoch}")
    m.train(mode=True)
    avg_loss = train_one_epoch(epoch, writer)
    m.train(mode=False)

    running_vloss = 0.0
    for i in range(len(data_validation)):
        vinputs, vlabels = x_validation[i], y_validation[i]
        voutputs = m(vinputs)
        vloss = loss_fn(voutputs, vlabels)
        running_vloss += vloss

        avg_vloss = running_vloss / (i + 1)
    print("LOSS train {} valid {}".format(avg_loss, avg_vloss))
    writer.add_scalars("Training vs Validation loss",
                       {"Training": avg_loss, "Validation": avg_vloss}, epoch)
    writer.flush()

    print(f"Avg vloss: {avg_vloss}\nBest vloss: {best_vloss}")
    if avg_vloss < best_vloss:
        best_vloss = avg_vloss
        torch.save(m.state_dict(), "scriptmodule_state_dict.pt")

# m = torch.jit.script(MyModule())
# m.register_parameter("test",Parameter(data=FakeTensor(FakeTensorMode(),MetaConverter(),torch.device)))
# for p in m.parameters():
#     print(p)
# Save to file

torch.jit.script(m).save('scriptmodule.pt')

# with open("strings.txt") as csv:
#     data = csv.readlines()
#     for line in data:
#         (x, y) = line.strip().split(",",maxsplit=2)
#         if x != y:
#             print(f"{x} != {y}")


# Flag: HV22{AA21B6AB-4520-4AD2-8016-4A9F2C371E6E}