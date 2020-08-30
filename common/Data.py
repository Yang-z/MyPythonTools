import json
import os

class Data:

    # Python, just can't update a value by passing it to a function...
    @staticmethod
    def load(
            # in_memory_data,
            path, store_method='json'
    ):
        if not os.path.exists(path): return None
        with open(path, 'r', encoding='utf-8') as f:
            fr = f.read()
            in_memory_data = json.loads(fr) \
                if store_method == 'json' \
                else eval(fr.lower())
        return in_memory_data

    @staticmethod
    def save(in_memory_data, path, store_method='json'):
        if in_memory_data is None: return
        with open(path, 'w', encoding='utf-8') as f:
            if store_method == 'json':
                f.write(json.dumps(
                    in_memory_data,
                    indent=4, separators=(',', ':'),
                    ensure_ascii=False
                ))
            else:
                f.write(str(in_memory_data))

    @staticmethod
    def solve_path(path_raw: str, para: dict={}) -> str:
        path_solved = path_raw
        for key in para:
            path_solved = path_solved.replace(f'${{{key}}}', para[key])
        return path_solved


if __name__ == '__main__':
    p = Data.solve_path(
        r"TeamDriveDict(${user}).json",
        {
            'user': "test@test.org"
        }
    )

    print("break here")
