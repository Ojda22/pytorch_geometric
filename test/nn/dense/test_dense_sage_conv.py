import torch

from torch_geometric.nn import DenseSAGEConv, SAGEConv


def test_dense_sage_conv():
    channels = 16
    sparse_conv = SAGEConv(channels, channels, normalize=True)
    dense_conv = DenseSAGEConv(channels, channels, normalize=True)
    assert dense_conv.__repr__() == 'DenseSAGEConv(16, 16)'

    # Ensure same weights and bias.
    dense_conv.lin_rel = sparse_conv.lin_l
    dense_conv.lin_root = sparse_conv.lin_r

    x = torch.randn((5, channels))
    edge_index = torch.tensor([[0, 0, 1, 1, 2, 2, 3, 4],
                               [1, 2, 0, 2, 0, 1, 4, 3]])

    sparse_out = sparse_conv(x, edge_index)
    assert sparse_out.size() == (5, channels)

    x = torch.cat([x, x.new_zeros(1, channels)], dim=0).view(2, 3, channels)
    adj = torch.Tensor([
        [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ],
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0],
        ],
    ])
    mask = torch.tensor([[1, 1, 1], [1, 1, 0]], dtype=torch.bool)

    dense_out = dense_conv(x, adj, mask)
    assert dense_out.size() == (2, 3, channels)

    assert dense_out[1, 2].abs().sum().item() == 0
    dense_out = dense_out.view(6, channels)[:-1]
    assert torch.allclose(sparse_out, dense_out, atol=1e-04)


def test_dense_sage_conv_with_broadcasting():
    batch_size, num_nodes, channels = 8, 3, 16
    conv = DenseSAGEConv(channels, channels)

    x = torch.randn(batch_size, num_nodes, channels)
    adj = torch.Tensor([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ])

    assert conv(x, adj).size() == (batch_size, num_nodes, channels)
    mask = torch.tensor([1, 1, 1], dtype=torch.bool)
    assert conv(x, adj, mask).size() == (batch_size, num_nodes, channels)
