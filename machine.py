import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from other_dates import stock_symbol
data1 = stock_symbol
try:
    data1 = np.array(data1)

    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(data1.reshape(-1, 1))

    def create_sequences(data, seq_length):
        sequences, labels = [], []
        for i in range(len(data) - seq_length):
            seq = data[i:i + seq_length]
            label = data[i + seq_length]
            sequences.append(seq)
            labels.append(label)
        return np.array(sequences), np.array(labels)

    seq_length = 10  
    sequences, labels = create_sequences(data_normalized, seq_length)


    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')


    X_train, y_train = sequences, labels
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))


    model.fit(X_train, y_train, epochs=50, batch_size=32)


    last_sequence = data_normalized[-seq_length:]
    last_sequence = last_sequence.reshape((1, seq_length, 1))

    predicted_value = model.predict(last_sequence)


    predicted_value = scaler.inverse_transform(predicted_value.reshape(1, -1))[0, 0]

except: 
    predicted_value = "Couldnt calculate the next value, try other date."
