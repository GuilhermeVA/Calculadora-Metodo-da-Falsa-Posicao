import streamlit as st
from sympy import symbols, sympify, lambdify

# python -m streamlit run falsa_posicao_app.py


def falsa_posicao(f, a, b, error, max_iter=100):
    x = symbols('x')
    f_expr = sympify(f)
    f_lamb = lambdify(x,f_expr)

    if f_lamb(a) * f_lamb(b) >= 0:
        raise ValueError("f(a) e f(b) devem ter sinais opostos")
    

    steps = []
    xr = None
    er = None
    for i in range(max_iter):
        old_x = xr
        fa = f_lamb(a)
        fb = f_lamb(b)
        xr= (a*fb - b*fa)/(fb-fa)
        fxr = f_lamb(xr)

        if i >= 1:
            er = abs((xr - old_x)/xr) * 100

        er_str = f"{er:.6f}" if er is not None else "N/A"
        steps.append(f"Iteração {i+1}: a={a:.6f} | b={b:.6f} | x{i}={xr:.6f} | f(x{i})={fxr:.6f} | er={er_str}")

        if er != None:
            if er < error:
                return f"xr={xr:.6f}", steps
                
        if fa * fxr < 0:
            b = xr
        
        elif fb * fxr < 0:
            a = xr

    return xr, steps



#Interface
st.set_page_config(page_title="Método da Falsa Posição", layout="centered")

st.title("Método da Falsa Posição")

st.markdown("""
Digite a função, os valores de **a** e **b**, e o **erro tolerável**.  
A função deve ser em termos de **x**.  
Exemplos válidos:
- `x**3 - 9*x + 3`
- `cos(x) - x`
- `x**2 - 4`
""")

funcao = st.text_input("Função em x:", value="x**3 - 9*x + 3")

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Valor de a:", value=0.0)
with col2:
    b = st.number_input("Valor de b:", value=1.0)

erro = st.number_input("Erro (%):", value=0.01, min_value=0.00001, format="%.5f")

if st.button("Calcular"):
    try:
        resultado, iteracoes = falsa_posicao(funcao, a, b, erro)

        st.success(resultado)
        st.subheader("Detalhes das Iterações:")
        for linha in iteracoes:
            st.text(linha)
        
    except Exception as e:
        st.error(f"Erro: {str(e)}")
