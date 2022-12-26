print('===== import =====')
import tensorflow.keras as keras

print('===== initialize =====')
model = keras.Sequential([
    keras.Input(shape=(3,)),
    keras.layers.Dense(16),
    keras.layers.Dense(64),
])

print('===== compile =====')
model.compile(loss='binary_crossentropy')

inputs = [
    [i/100, 0, 0] for i in range(100)
]
outputs = [
    [i/100, (i+1)%100/100, i*2%100/100, abs(i-50)/100] + [0]*60 for i in range(100)
]

print('===== fit =====')
model.fit(inputs, outputs, epochs=10)

print('===== predict =====')

def print_array(label, array):
    print(label, ' '.join([f'{i:>5.2f}' for i in array[0:8]]))

for i, o in zip(inputs[:16], outputs):
    print_array('i  ', i)
    print_array('o  ', o)
    o_p = model.predict([i], verbose=0)
    print_array('o_p', o_p[0])
    print()
