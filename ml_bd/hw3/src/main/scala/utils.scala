import breeze.linalg.{DenseMatrix, DenseVector}
import breeze.numerics.abs
import breeze.stats.mean
import models.LinearRegression

package object utils {
  def meanAbsoluteError(x: DenseVector[Double], y: DenseVector[Double]): Double = {
    mean(abs(x - y))
  }

  def crossValidation(model: LinearRegression, data: DenseMatrix[Double], numFolds: Int): Unit = {
    val step: Int = data.rows / numFolds

    for (i <- 0 until numFolds) {
      val trainIdx: IndexedSeq[Int] = IndexedSeq.range(0, i * step) ++ IndexedSeq.range((i + 1) * step, data.rows)
      val validIdx: IndexedSeq[Int] = IndexedSeq.range(i * step, (i + 1) * step)

      val train:  DenseMatrix[Double] = data(trainIdx, ::).toDenseMatrix
      val valid:  DenseMatrix[Double] = data(validIdx, ::).toDenseMatrix
      
      val xTrain: DenseMatrix[Double] = train(::, 0 to -2)
      val yTrain: DenseVector[Double] = train(::, -1)
      val xValid: DenseMatrix[Double] = valid(::, 0 to -2)
      val yValid: DenseVector[Double] = valid(::, -1)

      model.fit(xTrain, yTrain)

      val mae: Double = meanAbsoluteError(yValid, model.predict(xValid))
      println(s"${i+1} Fold: mae=$mae")
    }
  }
}