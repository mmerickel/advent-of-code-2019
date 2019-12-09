import numpy as np

def parse_image(data, width, height):
    layers = len(data) // (width * height)
    data = np.array([int(x) for x in data])
    data = data.reshape(layers, height, width)
    return data

def test_parse():
    data = parse_image('123456789012', 3, 2)
    np.testing.assert_array_equal(data, np.array([
        [[1, 2, 3], [4, 5, 6]],
        [[7, 8, 9], [0, 1, 2]],
    ]))

def find_layer_with_min_zeros(data):
    nonzero_per_layer = np.count_nonzero(data, (1, 2))
    best_layer_index = np.argmax(nonzero_per_layer)
    return data[best_layer_index]

def main():
    with open('p8.input') as fp:
        data = fp.read().strip()

    image = parse_image(data, 25, 6)
    layer = find_layer_with_min_zeros(image)
    layer = layer.flatten()
    num_ones = np.count_nonzero(layer == 1)
    num_twos = np.count_nonzero(layer == 2)
    print(num_ones * num_twos)

if __name__ == '__main__':
    main()
