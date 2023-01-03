import torch
import io

class MyModule(torch.nn.Module):
    def forward(self, x):
        return x + 10

m = torch.jit.script(MyModule())

# Save to file
torch.jit.save(m, 'scriptmodule.pt')
