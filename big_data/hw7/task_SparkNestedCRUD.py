from pyspark.sql.functions import struct
from pyspark.sql.types import StructField, StructType


def add_subtree(path, value):

    if not path:
        return value

    name, *path = path
    if not path:
        return value.alias(name)

    return struct(add_subtree(path, value)).alias(name)


def create_tree(df, path, struct_field, new_path, value):

    name, *new_path = new_path
    if isinstance(struct_field, StructField):
        if new_path:
            return struct(add_subtree(new_path, value)).alias(name)
        return add_subtree(new_path, value).alias(name)

    fields, found_field = [], False

    for field in struct_field.fields:
        if field.name == name:
            found_field = True
            if not new_path:
                fields.append(value.alias(name))
            else:
                if isinstance(field.dataType, StructType) and new_path:
                    fields.append(create_tree(
                        df=df,
                        path=f'{path}.{field.name}',
                        struct_field=field.dataType,
                        new_path=new_path,
                        value=value
                    ).alias(name))
                else:
                    if new_path:
                        fields.append(struct(add_subtree(new_path, value)).alias(name))
                    else:
                        fields.append(add_subtree(new_path, value).alias(name))
        else:
            fields.append(df[f'{path}.{field.name}'])

    if not found_field:
        fields.append(add_subtree(new_path, value).alias(name))

    return struct(*fields)


def _update_df(df, path, value):

    name, *path = path.split('.')

    for field in df.schema.fields:
        if field.name == name:
            if path:
                columns = create_tree(
                    df=df,
                    path=name,
                    struct_field=field.dataType,
                    new_path=path,
                    value=value
                )
                break
            columns = add_subtree(path, value)
    else:
        if path:
            columns = struct(add_subtree(path, value)).alias(name)
        else:
            columns = add_subtree(path, value)

    return df.withColumn(name, columns)


def update_df(df, columns_dict):

    updated_df = df

    for path, value in columns_dict.items():
        updated_df = _update_df(updated_df, path, value)

    return updated_df
