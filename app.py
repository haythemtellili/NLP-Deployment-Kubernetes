import os
import torch
import flask
import numpy as np
from flask import Flask, request

import config as config
from utils import LabelEncoder
from model import MultilabelClassifier


app = Flask("app")

DEVICE = config.DEVICE
label_encoder = LabelEncoder.load(
    os.path.join(config.PATH_MODELS, config.LABEL_ENCODER_PATH)
)
n_classes = len(label_encoder)
MODEL = MultilabelClassifier(n_classes)
MODEL.load_state_dict(
    torch.load(
        os.path.join(config.PATH_MODELS, config.BERT_PATH),
        map_location=torch.device(DEVICE),
    )
)
MODEL.to(DEVICE)
MODEL.eval()


def url_prediction(url):
    """Funcion that takes a url and return prediction"""
    tokenizer = config.TOKENIZER
    max_len = config.MAX_LEN
    url = str(url)
    url = " ".join(url.split())
    inputs = tokenizer.encode_plus(
        url,
        None,
        add_special_tokens=True,
        max_length=max_len,
        pad_to_max_length=True,
        truncation=True,
    )

    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]

    ids = torch.tensor(ids, dtype=torch.long).unsqueeze(0)
    mask = torch.tensor(mask, dtype=torch.long).unsqueeze(0)

    ids = ids.to(DEVICE, dtype=torch.long)
    mask = mask.to(DEVICE, dtype=torch.long)

    outputs = MODEL(ids=ids, mask=mask)
    outputs = torch.sigmoid(outputs).cpu().detach().numpy()
    return outputs


@app.route("/predict", methods=["GET"])
def predict():
    url = request.args.get("url")
    output = url_prediction(url)
    result = np.array([np.where(prob >= config.THRESHOLD, 1, 0) for prob in output])
    response = {}
    response["response"] = {
        "tags": str(label_encoder.decode([result[0]])[0]),
        "url": str(url),
    }
    return flask.jsonify(response)


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port="9999")