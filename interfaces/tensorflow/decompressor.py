print('===== import =====')
import tensorflow.keras as keras

print('===== initialize =====')
model = keras.Sequential([
    keras.Input(shape=(3,)),
    keras.layers.Dense(64),
])

print('===== compile =====')
model.compile(loss='binary_crossentropy')

inputs = [
    [i, 0, 0] for i in range(256)
]
outputs = [
    [i, i+1, i*2, abs(i-128)] + [0]*60 for i in range(256)
]

print('===== fit =====')
model.fit(inputs, outputs)

print('===== predict =====')
for i, o in zip(inputs[:16], outputs):
    print(i)
    print(o[0:5])
    o_p = model.predict([i], verbose=0)
    print([int(i*10)/10 for i in o_p[0][0:5]])
