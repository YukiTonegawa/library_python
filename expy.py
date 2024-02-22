import sys
import os
import pathlib

"""
Python3 expy.py aaa.py

from libfile import * 
の形式でインポートされたカレントディレクトリ下のファイルを展開

注: 
    ダブルクオーテーション3つでコメントアウトされた中にあるものも展開される(#は展開されない)
    sys.path.appendなどでモジュールの検索対象のディレクトリをいじれるが, libfileの名称は本体のコードに対する相対パスでないとならない
"""

def invalid_args(S) -> None:
    print(S)
    print("Python3 expy.py aaa.py")
    exit(1)

# aaa.pyが有効か確認
# 有効な場合, aaa.pyのフルパスを返す
def check() -> str:
    if(len(sys.argv) != 2):
        invalid_args("Error")
    
    code_name = sys.argv[1]
    tmp = os.path.splitext(code_name)

    if tmp[1] != ".py":
        invalid_args(code_name + " is not python file")

    code_path = os.path.join(os.getcwd(), code_name)
    
    if not os.path.isfile(code_path):
        invalid_args('There is no python code named ' + code_name)

    return code_path

# code_pathに含まれる依存先のフルパスを列挙
def find_dependency(code_path) -> set:
    libs = set()
    with open(code_path) as f:
        for S in f.readlines():
            sp = S.split()
            if len(sp) == 0 or sp[0] != "from":
                continue
            lib_name = sp[1]
            prefix_comma = 0
            for c in lib_name:
                if c == '.':
                    prefix_comma += 1
                else:
                    break
            
            lib_path = os.path.dirname(code_path)

            lib_name = lib_name[prefix_comma : ].replace('.', '/') + ".py"

            if prefix_comma <= 1:
                lib_path = os.path.join(lib_path, lib_name)
            else:
                p = pathlib.Path(lib_path).parents[prefix_comma - 2]
                lib_path = os.path.join(str(p), lib_name)
            
            if os.path.isfile(lib_path):
                libs.add(lib_path)
                print(code_path, '<-', lib_path)
    return libs

# DAGの親から順序を決定
# 相互参照していると壊れる
def find_dependency_recursive(code_path) -> list:
    par = dict()
    st = [code_path]
    while st:
        v = st[-1]
        st.pop()
        if v in par:
            continue
        L = find_dependency(v)
        par[v] = L
        for p in L:
            if p in par:
                continue
            st.append(p)
    
    res = []
    while par:
        s = ""
        for c, ps in par.items():
            if len(ps):
                continue
            s = c
            break
        if len(s) == 0:
            assert "Error: cross-reference found"
        
        res.append(s)
        del par[s]
        for c, ps in par.items():
            if s in ps:
                ps.remove(s)
    return res
    

# 展開されたライブラリに対するimport文を消す
def modify_import(code_path) -> str:
    res = []
    with open(code_path) as f:
        for S in f.readlines():
            sp = S.split()
            if len(sp) == 0 or sp[0] != "from":
                res.append(S)
                continue
            lib_name = sp[1]
            prefix_comma = 0
            for c in lib_name:
                if c == '.':
                    prefix_comma += 1
                else:
                    break
            
            lib_path = os.path.dirname(code_path)

            lib_name = lib_name[prefix_comma : ].replace('.', '/') + ".py"

            if prefix_comma <= 1:
                lib_path = os.path.join(lib_path, lib_name)
            else:
                p = pathlib.Path(lib_path).parents[prefix_comma - 2]
                lib_path = os.path.join(str(p), lib_name)

            if not os.path.isfile(lib_path):
                res.append(S)
    return ''.join(res) + '\n'

# output_fileを消す
def clear_output(output_file) -> None:
    if os.path.isfile(output_file):
        os.remove(output_file)

# 展開
def expand(code_path, output_file) -> None:
    clear_output(output_file)
    with open(output_file, mode='w') as o:
        v = find_dependency_recursive(code_path)
        for lib_path in v:
            s = modify_import(lib_path)
            o.write(s)

OUTFILE = "expanded.py"
def main():
    code_path = check()
    expand(code_path, OUTFILE)

main()

