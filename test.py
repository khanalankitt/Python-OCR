# Test CUDA for hardware acceleration
# Model works faster with GPU than CPU
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"Number of GPUs: {torch.cuda.device_count()}")
print(f"Current GPU: {torch.cuda.current_device()}")
print(f"GPU Name: {torch.cuda.get_device_name(torch.cuda.current_device())}")