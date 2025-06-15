import streamlit as st
from collections import deque

memory = [0] * 30000
pointer = 0
input_index = 0
input_str = ""
output = ""
loop_stack = deque()
tf = 1
def run_brainfuck(start,goal):
    global input_index,pointer,output
    _ = start
    while _ < goal:
        cmd = code[_]        
        if cmd == '>':
            pointer += 1
        elif cmd == '<':
            pointer -= 1
        elif cmd == '+':
            memory[pointer] = (memory[pointer] + 1) % 256
        elif cmd == '-':
            memory[pointer] = (memory[pointer] - 1) % 256
        elif cmd == '.':
            output += chr(memory[pointer])
        elif cmd == ',':
            if input_index < len(input_str):
                memory[pointer] = ord(input_str[input_index])
                input_index += 1
            else:
                memory[pointer] = 0
        elif cmd == '[':
            count_k = 1
            for end in range(_+1,goal):
                now = code[end]
                if now == "[":
                    count_k += 1
                elif now == "]":
                    count_k -= 1
                    if count_k == 0:
                        break
            while memory[pointer]:
                run_brainfuck(_+1,end)
            _ = end 
        _ += 1    


st.title("Brainfuck Editor & Memory Viewer")

code = st.text_area("Brainfuck Code", value="")
input_str = st.text_area("Input", "")
run = st.button("Run")

if run:
    output = ""
    run_brainfuck(0,len(code))
    st.subheader("Output")
    st.code(output)

    st.subheader("Memory (First 20 cells)")
    import pandas as pd

    # 数値 → 文字（表示可能範囲のみ、それ以外は "." に）
    mem_view = [memory[i] for i in range(20)]
    mem_chars = [chr(v) if 32 <= v <= 126 else '' for v in mem_view]
    if pointer < 20:
        mem_pointer = ["✓" if i == pointer else "" for i in range(len(mem_view))]
    else:
        mem_pointer = [""]*20

    df = pd.DataFrame([mem_view, mem_chars,mem_pointer], index=["値", "文字","位置"])
    df.columns = [f"{i}" for i in range(len(mem_view))]

    st.table(df)


    st.write(f"Pointer Position: {pointer}")
