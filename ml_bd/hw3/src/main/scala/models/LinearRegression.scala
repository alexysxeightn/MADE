package models

import breeze.linalg.{DenseMatrix, DenseVector, inv}

class LinearRegression {
  var w: DenseVector[Double] = DenseVector.zeros[Double](size = 0)

  def fit(X: DenseMatrix[Double], y: DenseVector[Double]): Unit = {
    w = inv(X.t * X) * X.t * y
  }

  def predict(X: DenseMatrix[Double]): DenseVector[Double] = {
    X * w
  }
}