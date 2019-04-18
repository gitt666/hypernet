import numpy as np
import torch

from python_research.experiments.hsi_attention.models.util import build_convolutional_block, AttentionBlock, \
    build_classifier_block, \
    build_classifier_confidence


class Model2(torch.nn.Module):

    def __init__(self, num_of_classes: int, input_dimension: int, uses_attention: bool = False):
        super().__init__()
        self._conv_block_1 = build_convolutional_block(1, 96)
        self._conv_block_2 = build_convolutional_block(96, 54)
        self._attention_block_1 = AttentionBlock(96, int(input_dimension / 2), num_of_classes)
        self._attention_block_2 = AttentionBlock(54, int(input_dimension / 4), num_of_classes)
        self._classifier = build_classifier_block(54 * int(input_dimension / 4), num_of_classes)
        self._classifier_confidence = build_classifier_confidence(54 * int(input_dimension / 4))
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.0001)
        self.loss = torch.nn.CrossEntropyLoss()
        self.uses_attention = uses_attention

    def forward(self, x: torch.Tensor, y: torch.Tensor, infer: bool):
        global first_module_prediction, second_module_prediction
        z = self._conv_block_1(x)
        if self.uses_attention:
            first_module_prediction = self._attention_block_1(z, y, infer)
        z = self._conv_block_2(z)
        if self.uses_attention:
            second_module_prediction = self._attention_block_2(z, y, infer)
        prediction = self._classifier(z.view(z.shape[0], -1)) * \
                     self._classifier_confidence(z.view(z.shape[0], -1))
        if self.uses_attention:
            return prediction + first_module_prediction + second_module_prediction
        return prediction

    def get_heatmaps(self, input_size: int):
        return np.mean([self._attention_block_1.get_heatmaps(input_size).squeeze(),
                        self._attention_block_2.get_heatmaps(input_size).squeeze()], axis=0).squeeze()
