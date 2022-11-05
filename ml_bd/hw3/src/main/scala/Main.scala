import breeze.linalg.{csvread, csvwrite, DenseMatrix, DenseVector}
import java.io.File
import models.LinearRegression
import utils.crossValidation


object Main {
  def main(args: Array[String]): Unit = {
    if (args.length != 3) {
      println("Ожидались 3 параметра (путь до тренировочных данных, тестовых и для предсказания модели)")
      return
    }

    val trainPath:  File = new File(args(0))
    val testPath:   File = new File(args(1))
    val outputPath: File = new File(args(2))

    val train: DenseMatrix[Double] = csvread(trainPath, separator = ',', skipLines = 1)
    val test:  DenseMatrix[Double] = csvread(testPath,  separator = ',', skipLines = 1)

    val xTrain: DenseMatrix[Double] = train(::, 0 to -2)
    val yTrain: DenseVector[Double] = train(::, -1)

    val model = new LinearRegression()
    crossValidation(model, train, numFolds = 5)
    model.fit(xTrain, yTrain)

    val prediction: DenseVector[Double] = model.predict(test)
    csvwrite(outputPath, prediction.asDenseMatrix.t)
  }
}