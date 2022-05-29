import logging
import os
import pickle
from pydantic import BaseModel
from typing import List, Optional

from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn

from src.preprocessing import CustomTransformerClass
from src.models.train_model import SklearnClassifierModel


model: Optional[SklearnClassifierModel] = None
transformer: Optional[CustomTransformerClass] = None

logger = logging.getLogger(__name__)
app = FastAPI()


class HeartDataModel(BaseModel):
	id: int
	age: int
	sex: int
	cp: int
	trestbps: int
	chol: int
	fbs: int
	restecg: int
	thalach: int
	exang: int
	oldpeak: float
	slope: int
	ca: int
	thal: int


class HeartResponse(BaseModel):
	id: int
	condition: int


def load_object(path: str) -> dict:
	with open(path, "rb") as f:
		return pickle.load(f)


def make_prediction(
	data: List[HeartDataModel],
	model: SklearnClassifierModel,
	transformer: CustomTransformerClass
) -> List[HeartResponse]:
	df = pd.DataFrame(dict(x) for x in data)
	transformed_data = transformer.transform(df.drop('id', axis=1))
	prediction = model.predict(transformed_data)
	return [
		HeartResponse(id=id, condition=condition)
		for id, condition in zip(df['id'], prediction)
	]


@app.on_event("startup")
def load_model():
	global model, transformer

	model_path = os.getenv("PATH_TO_MODEL", default="artifacts/model.pkl")
	transformer_path = os.getenv("PATH_TO_TRANSFORMER", default="artifacts/transformer.pkl")
	
	try:
		model = load_object(model_path)
		transformer = load_object(transformer_path)
	except FileNotFoundError as e:
		logger.error(e)
		return


@app.get("/")
def main():
	return "Hi! I'm Work!"


@app.get("/health/")
def health() -> bool:
	return (model is not None) and (transformer is not None)


@app.post("/predict/", response_model=List[HeartResponse])
def predict(request: List[HeartDataModel]):
	if not health():
		logger.error("Model or transformer is not loaded")
		raise HTTPException(status_code=500)

	return make_prediction(request, model, transformer)


if __name__ == '__main__':
	uvicorn.run("app:app", host="0.0.0.0", port=os.getenv("PORT", 8000))
