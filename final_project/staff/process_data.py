from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, to_date
import sys

def main():
    spark = SparkSession.builder \
        .appName("FamilyDataProcessing") \
        .config("spark.hadoop.fs.s3a.endpoint", "storage.yandexcloud.net") \
        .getOrCreate()

    try:
        args = {k: v for k, v in zip(sys.argv[1::2], sys.argv[2::2])}
        input_path = args.get('--input', 's3://examen/file/family.csv')
        output_path = args.get('--output', 's3://examen/results/family_processed')

        # Чтение данных с явным указанием схемы
        df = spark.read.csv(input_path, header=False, schema="id INT, date STRING, name STRING, is_male BOOLEAN")
        
        # Преобразование даты (формат: "1993-04-14 00:00:00 +0000 UTC")
        df = df.withColumn("date", to_date(col("date").substr(1, 10), "yyyy-MM-dd"))
        
        # Проверка данных
        print("Пример данных:")
        df.show(5, truncate=False)
        
        # Фильтрация и агрегация
        result_df = df.filter(year(col("date")) >= 2001) \
                    .groupBy("is_male") \
                    .count()
        
        # Сохранение
        result_df.write.mode("overwrite").parquet(output_path)
        print(f"Результат сохранен в {output_path}")
        return 0

    except Exception as e:
        print(f"Ошибка: {str(e)}", file=sys.stderr)
        return 1
    finally:
        spark.stop()

if __name__ == "__main__":
    sys.exit(main())