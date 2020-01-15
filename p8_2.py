import numpy as np

def parse_image(data, width, height):
    layers = len(data) // (width * height)
    data = np.array([int(x) for x in data])
    data = data.reshape(layers, height, width)
    return data

def flatten_layers(image):
    result = image[-1]
    for layer in reversed(image):
        np.putmask(result, layer != 2, layer)
    return result

def render_layer(layer):
    return '\n'.join(
        ''.join(str(x) for x in row)
        for row in layer
    )

def test_parse():
    data = parse_image('0222112222120000', 2, 2)
    np.testing.assert_array_equal(data, np.array([
        [[0, 2], [2, 2]],
        [[1, 1], [2, 2]],
        [[2, 2], [1, 2]],
        [[0, 0], [0, 0]],
    ]))

def test_flatten():
    data = parse_image('0222112222120000', 2, 2)
    result = flatten_layers(data)
    np.testing.assert_array_equal(result, np.array([
        [0, 1], [1, 0],
    ]))

def test_render():
    layer = [
        [0, 1], [1, 0],
    ]
    result = render_layer(layer)
    assert result == '01\n10'

def main():
    with open('p8.input') as fp:
        data = fp.read().strip()

    image = parse_image(data, 25, 6)
    layer = flatten_layers(image)
    result = render_layer(layer)
    print(result.replace('0', ' '))

if __name__ == '__main__':
    main()
