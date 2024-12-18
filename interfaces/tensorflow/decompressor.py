inputs = [
    [i/100, 0, 0] for i in range(100)
]
outputs = [
    [i/100, min(1, (i+10)/100), min(1, i*2/100), abs(i-50)/100] + [0]*60 for i in range(100)
]

print('===== import =====')
import tensorflow.keras as keras

print('===== initialize =====')
model = keras.Sequential([
    keras.Input(shape=(len(inputs[0]),)),
    keras.layers.Dense(64),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(len(outputs[0])),
])

print('===== compile =====')
model.compile(loss='mean_squared_error')

print('===== fit =====')
model.fit(
    inputs,
    outputs,
    epochs=500,
    callbacks=[keras.callbacks.LambdaCallback(lambda epoch, logs: print(epoch))],
    verbose=0,
)

print('===== predict =====')
predictions = model.predict(inputs, verbose=0)

print('===== plot =====')
import dansplotcore as dpc
plot = dpc.Plot(
    transform=dpc.t.Default([
        dpc.t.Color(255, 0, 0), dpc.t.Color(128, 0, 0),
        dpc.t.Color(0, 255, 0), dpc.t.Color(0, 128, 0),
        dpc.t.Color(0, 0, 255), dpc.t.Color(0, 0, 128),
        dpc.t.Color(255, 255, 255), dpc.t.Color(128, 128, 128),
        dpc.t.Color(255, 255, 0), dpc.t.Color(128, 128, 0),
    ]),
    primitive=dpc.p.Plus(),
)
for j in range(5):
    plot.plot([i[0] for i in inputs], [i[j] for i in outputs])
    plot.plot([i[0] for i in inputs], [float(i[j]) for i in predictions])
plot.show()
