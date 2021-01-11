"Updated version"

import ast
import types
import sys
import numpy as np


prefix = "import os\nfrom torchvision import transforms\nfrom torchvision.datasets import MNIST, FashionMNIST\nfmnist_train = FashionMNIST(os.getcwd(), train=True, download=True, transform=transforms.ToTensor())\n"
with open("rapport.py") as f:
    p = ast.parse(prefix + f.read())

for node in p.body[:]:
    if not isinstance(node, (ast.FunctionDef, ast.Import, ast.ImportFrom, ast.Assign)):
        p.body.remove(node)

module = types.ModuleType("mod")
code = compile(p, "mod.py", "exec")
sys.modules["mod"] = module
exec(code, module.__dict__)
from mod import *

# from rapport import build_image_like_tensor, normalize_tensor, sigmoid, softmax
# from rapport import (
#    R_0,
#    R_1,
#    convolution_forward_numpy,
#    convolution_forward_torch,
#    fashion_mnist_dataset_answer,
#    target_to_one_hot,
# )


def test_build_image_like_tensor():
    matrix = build_image_like_tensor(320, 240, 3, 1)
    assert matrix.shape == (320, 240, 3)
    assert np.allclose(matrix, np.full((320, 240, 3), 1))
    matrix = build_image_like_tensor(20, 40, 1, 10)
    assert matrix.shape == (20, 40, 1)
    assert np.allclose(matrix, np.full((20, 40, 1), 10))


def test_normalize():
    arr = np.arange(6).reshape(2, -1)
    arr_test = arr / 255
    assert np.allclose(normalize_tensor(arr), arr_test)


def test_one_hot():
    arr = np.array([0, 1, 9])
    arr_test = np.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ]
    )
    assert np.allclose(target_to_one_hot(arr), arr_test)


def test_sigmoid():
    arr = np.arange(6).reshape(2, -1)
    arr_test = np.array(
        [[0.5, 0.73105858, 0.88079708], [0.95257413, 0.98201379, 0.99330715]]
    )
    assert np.allclose(sigmoid(arr), arr_test)


def test_softmax():
    arr = np.arange(6).reshape(2, -1)
    arr_test = np.array(
        [[0.09003057, 0.24472847, 0.66524096], [0.09003057, 0.24472847, 0.66524096]]
    )
    assert np.allclose(softmax(arr), arr_test)


def test_R0():
    arr_test = np.array(
        [
            [0, 0, 0, 0, 0],
            [252, 49, 113, 11, 137],
            [18, 237, 163, 119, 53],
            [90, 89, 178, 75, 247],
            [209, 216, 48, 135, 232],
        ]
    )
    assert np.allclose(R_0, arr_test)


def test_R1():
    arr_test = np.array(
        [
            [1005, -173, 46, -280, 513],
            [212, 1242, 646, 356, 91],
            [280, 390, 1010, 295, 1040],
            [942, 1048, 316, 740, 1154],
            [1570, 738, 934, 945, 1477],
        ]
    )
    assert np.allclose(R_1, arr_test)


def test_convolution_numpy():
    K_0 = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]])
    K_1 = np.array([[1, 1, 1], [0, 5, 0], [-1, -1, -1]])

    I = np.array(
        [
            [252, 49, 113, 11, 137],
            [18, 237, 163, 119, 53],
            [90, 89, 178, 75, 247],
            [209, 216, 48, 135, 232],
            [229, 53, 107, 106, 222],
        ]
    )

    expected_test_K0 = np.array(
        [
            [0, 0, 0, 0, 0],
            [252, 49, 113, 11, 137],
            [18, 237, 163, 119, 53],
            [90, 89, 178, 75, 247],
            [209, 216, 48, 135, 232],
        ]
    )

    expected_test_K1 = np.array(
        [
            [1005, -173, 46, -280, 513],
            [212, 1242, 646, 356, 91],
            [280, 390, 1010, 295, 1040],
            [942, 1048, 316, 740, 1154],
            [1570, 738, 934, 945, 1477],
        ]
    )

    student_result_K0 = convolution_forward_numpy(I, K_0)
    student_result_K1 = convolution_forward_numpy(I, K_1)
    assert np.allclose(expected_test_K0, student_result_K0)
    assert np.allclose(expected_test_K1, student_result_K1)


def test_convolution_torch():
    image = np.ones((10, 10))
    kernel = np.array([[0, 2, 0], [0, 1, 0], [0, 1, 0]])

    expected_result = np.full((10, 10), 4)
    student_result = convolution_forward_torch(image, kernel)
    assert np.allclose(expected_result, student_result)


def test_fashion_mnist_dataset_answer():

    student_result = fashion_mnist_dataset_answer()
    assert np.allclose(student_result["shape"], 1)
    assert np.allclose(student_result["nb_in_train_set"], 1)
    assert np.allclose(student_result["nb_in_test_set"], 1)
    assert np.allclose(student_result["number_of_classes"], 1)
