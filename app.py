import streamlit as st
import plotly.express as px
import conn
import funcs as fc

# Interface do Streamlit
def main():

    st.set_page_config(page_title='Meus gastos', page_icon=':moneybag:', layout='wide')

    service = conn.get_service()

    data_mika, data_mae, data_saldo, data_proventos = conn.read_sheet(service, 'gastosmika'), conn.read_sheet(service, 'gastosmae'), conn.read_sheet_saldo(service, 'saldo'), conn.read_sheet(service, 'proventos')

    ano = fc.ano_atual()

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    with st.container():

        resumo, dados = st.columns([0.9, 0.1])

        with resumo:
              
            st.subheader('Métricas', divider='blue')

            with st.container():

                saldo_atual, saldo_emprestado, prov_previsto, deb_previsto, saldo_previsto, saldo_total_previsto = st.columns(6)

                with saldo_atual:

                    st.metric('Saldo atual', fc.formatar_valor_brasileiro(fc.saldo_atual(data_saldo)))

                with saldo_emprestado:
                    
                    st.metric('Saldo emprestado', fc.formatar_valor_brasileiro(fc.saldo_emprestado(data_saldo)))

                with prov_previsto:
                    
                    st.metric('Prov. Previsto', fc.formatar_valor_brasileiro(fc.prov_previsto(data_saldo)))

                with deb_previsto:

                    st.metric('Déb. Previsto', fc.formatar_valor_brasileiro(fc.deb_previsto(data_saldo)))
                
                with saldo_previsto:
                    saldo_atual = fc.saldo_atual(data_saldo)
                    proximas_faturas = fc.proximas_faturas(data_mika)
                    fatura_atual = fc.fatura_atual(data_mika)

                    saldo_previsto =  saldo_atual - (proximas_faturas + fatura_atual)

                    st.metric('Saldo previsto', fc.formatar_valor_brasileiro(saldo_previsto), help='Saldo atual descontado a fatura atual e as próximas')
                
                with saldo_total_previsto:

                    saldo_total_previsto = (fc.saldo_atual(data_saldo) + fc.saldo_emprestado(data_saldo) + fc.prov_previsto(data_saldo)) - (fc.deb_previsto(data_saldo) + fc.fatura_atual(data_mika) +  fc.proximas_faturas(data_mika))

                    st.metric('Saldo total previsto', fc.formatar_valor_brasileiro(saldo_total_previsto), help='Valores totais previstos descontado a fatura atual, próximas e déb. previsto')
            
            st.subheader('Faturas', divider='blue')
            
            with st.container():
                
                fatura_atual_anterior, fatura_proxima, fatura_mae, fatura_total = st.columns(4)

                with fatura_atual_anterior:
                    st.metric('Fatural atual', fc.formatar_valor_brasileiro(fc.fatura_atual(data_mika)))
                    st.metric('Fatura anterior', fc.formatar_valor_brasileiro(fc.fatura_anterior(data_mika)))

                with fatura_proxima:
                    st.metric('Próxima fatura', fc.formatar_valor_brasileiro(fc.fatura_proxima(data_mika)))
                    st.metric('Proximas faturas', fc.formatar_valor_brasileiro(fc.proximas_faturas(data_mika)), help='Soma dos próximos meses incluindo o mes seguinte')
                    
                with fatura_mae:
                    st.metric('Fatural atual mãe', fc.formatar_valor_brasileiro(fc.fatura_atual(data_mae)))
                    st.metric('Fatura anterior mãe', fc.formatar_valor_brasileiro(fc.fatura_anterior(data_mae)))

                with fatura_total:
                    fatura_total = fc.fatura_atual(data_mika) + fc.fatura_atual(data_mae)
                    fatura_total_anterior = fc.fatura_anterior(data_mika) + fc.fatura_anterior(data_mae)
                    st.metric('Fatura total atual', fc.formatar_valor_brasileiro(fatura_total), help='Fatural atual acrescido da fatura da mãe')
                    st.metric('Fatura total anterior', fc.formatar_valor_brasileiro(fatura_total_anterior), help='Fatural anterior acrescido da fatura da mãe')

        with dados:

            st.subheader('Registros', divider='blue')

            with st.popover("Fatura", use_container_width=True):


                with st.form(key='form_adicionar_dados', border= False):
                    
                    tabela = st.radio('Escolha a planilha', ('Mikael', 'Mãe'), horizontal=True)
                
                    coluna1, coluna2 = st.columns(2)
                
                    with coluna1:
                        dia = st.text_input('Dia')
                    with coluna2:
                        mes = st.text_input('Mês')
                    
                    descricao = st.text_input('Descrição')
                    valor = st.text_input('Valor')
                    parcelas = st.text_input('Parcelas', value='1')
                    classificacao = st.selectbox('Digite a classificação', conn.read_sheet(service, 'gastosmika')['classificacao'].unique())

                    submit_button = st.form_submit_button('Adicionar')

                    if submit_button:

                        dados = [f'{dia}/{mes}/{ano}', descricao, valor, parcelas, classificacao]

                        # Verifica se todos os campos estão preenchidos
                        if all(dados):

                            if tabela == 'Mikael':

                                for i in range(int(parcelas)):

                                    if i == 0:
                                        dados = [f'{dia}/{mes}/{ano}', descricao, round(float(valor.replace(',','.'))/int(parcelas), 2), f'{i+1}/{parcelas}', classificacao]
                                        conn.append_data(service, dados, 'gastosmika')

                                    else:
                                        # Cálculo para o mês atual, levando em consideração que pode passar de 12 (próximo ano)
                                        mes_parcela = (int(mes) + i - 1) % 12 + 1
                                        ano_parcela = int(ano) + (int(mes) + i - 1) // 12  # Incrementa o ano se o mês passar de 12

                                        # Formatação da descrição e valores para cada parcela
                                        n_parcelas = f'{i+1}/{parcelas}'
                                        valor_parcela = round(float(valor.replace(',','.'))/int(parcelas), 2)

                                        data = f'{2}/{mes_parcela}/{ano_parcela}'

                                        # Adiciona os dados formatados para cada parcela na lista
                                        dados = [data, descricao, valor_parcela, n_parcelas, classificacao]
                                        conn.append_data(service, dados, 'gastosmika')

                            else:

                                for i in range(int(parcelas)):

                                    if i == 0:
                                        dados = [f'{dia}/{mes}/{ano}', descricao, round(float(valor.replace(',','.'))/int(parcelas), 2), f'{i+1}/{parcelas}', classificacao]
                                        conn.append_data(service, dados, 'gastosmae')

                                    else:
                                        # Cálculo para o mês atual, levando em consideração que pode passar de 12 (próximo ano)
                                        mes_parcela = (int(mes) + i - 1) % 12 + 1
                                        ano_parcela = int(ano) + (int(mes) + i - 1) // 12  # Incrementa o ano se o mês passar de 12

                                        # Formatação da descrição e valores para cada parcela
                                        n_parcelas = f'{i+1}/{parcelas}'
                                        valor_parcela = round(float(valor.replace(',','.'))/int(parcelas), 2)

                                        data = f'{2}/{mes_parcela}/{ano_parcela}'

                                        # Adiciona os dados formatados para cada parcela na lista
                                        dados = [data, descricao, valor_parcela, n_parcelas, classificacao]
                                        conn.append_data(service, dados, 'gastosmae')

                        
                            st.success('Dados adicionados com sucesso!')
                            st.rerun()

                        else:
                            st.error('Preencha todos os campos!')

            with st.popover("Transação", use_container_width=True):

                with st.form(key='form_registro', border= False):
                    
                    tabela = st.radio('Escolha o tipo de transação', ('Provento', 'Débito', 'Empréstimo', 'Devolução', 'Deb. Previsto', 'Prov. Previsto'), horizontal=True)

                    coluna1, coluna2 = st.columns(2)
                
                    with coluna1:
                        dia = st.text_input('Dia')
                    with coluna2:
                        mes = st.text_input('Mês')

                    valor = st.text_input('Valor')

                    descricao = st.text_input('Descrição')

                    submit_button = st.form_submit_button('Adicionar')
                    
                    provento, debito, emprestimo, devolucao, deb_previsto, prov_previsto = '0', '0', '0', '0', '0', '0'

                    dados = [f'{dia}/{mes}/{ano}', provento, debito, emprestimo, devolucao, deb_previsto, prov_previsto, f'{tabela}: {descricao}']
                    
                    if submit_button:


                        if all(dados):

                            if tabela == 'Provento':
                                dados[1] = valor
                                conn.append_data(service, dados, 'saldo')
                           
                            elif tabela == 'Débito':
                                dados[2] = valor
                                conn.append_data(service, dados, 'saldo')
                            
                            elif tabela == 'Empréstimo':
                                dados[3] = valor
                                conn.append_data(service, dados, 'saldo')

                            elif tabela == 'Devolução':
                                dados[1], dados[4] = valor, valor
                                conn.append_data(service, dados, 'saldo')
                            
                            elif tabela == 'Deb. Previsto':
                                dados[5] = valor
                                conn.append_data(service, dados, 'saldo')
                            
                            else:
                                dados[6] = valor
                                conn.append_data(service, dados, 'saldo')

                            st.success('Dados adicionados com sucesso!')
                            st.rerun()

                        else:
                            st.error('Preencha todos os campos!')

    

    st.subheader('Ultimos gastos', divider='blue')

    with st.container():

        tab_gasto_mikael, tab_gasto_mae = st.columns(2)

        with tab_gasto_mikael:
            st.markdown(
            """
            <div style="display: flex; justify-content: left; align-items: center; height: 100%;">
            <h6 style="text-align: center;">Mikael</h6>
            </div>
            """, unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='display: inline-block; margin-right: 15px;'><strong>Data:</strong> {fc.ultimo_gasto_mes(data_mika).iloc[-1]['data'].strftime('%d/%m/%Y')}</p>"
                f"<p style='display: inline-block; margin-right: 15px;'><strong>Descrição:</strong> {fc.ultimo_gasto_mes(data_mika).iloc[-1]['descricao']}</p>"
                f"<p style='display: inline-block;'><strong>Valor:</strong> {str(fc.ultimo_gasto_mes(data_mika).iloc[-1]['valor']).replace('.', ',')}</p>",
                unsafe_allow_html=True
            )

        with tab_gasto_mae:

            st.markdown(
            """
            <div style="display: flex; justify-content: left; align-items: center; height: 100%;">
                <h6 style="text-align: center;">Mãe</h6>
            </div>
            """, unsafe_allow_html=True
            )

            st.markdown(
                f"<p style='display: inline-block; margin-right: 15px;'><strong>Data:</strong> {fc.ultimo_gasto_mes(data_mae).iloc[-1]['data'].strftime('%d/%m/%Y')}</p>"
                f"<p style='display: inline-block; margin-right: 15px;'><strong>Descrição:</strong> {fc.ultimo_gasto_mes(data_mae).iloc[-1]['descricao']}</p>"
                f"<p style='display: inline-block;'><strong>Valor:</strong> {str(fc.ultimo_gasto_mes(data_mae).iloc[-1]['valor']).replace('.', ',')}</p>",
                unsafe_allow_html=True
            )

    st.subheader('Gráficos', divider='blue')

    with st.container():

        tab_graf1, tab_graf2, tab_graf3 = st.columns([0.5,0.25, 0.25])
        
        with tab_graf1:
            st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <h6 style="text-align: center;">Gastos por periodo</h6>
            </div>
            """, unsafe_allow_html=True
            )
            fig2 = px.area(x=fc.soma_valores_por_mes(data_mika).index.astype(str), y=fc.soma_valores_por_mes(data_mika).values)
            st.plotly_chart(fig2, use_container_width=True)

            #fc.soma_valores_proventos_por_mes(data_mika, data_proventos) nao esta funcionando ver dps


        with tab_graf2:
            st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <h6 style="text-align: center;">Gastos por classificação</h6>
            </div>
            """, unsafe_allow_html=True
            )
            fig2 = px.bar(x=fc.soma_valores_por_classificacao(data_mika).sort_values(ascending=True).values, y=fc.soma_valores_por_classificacao(data_mika).sort_values(ascending=True).index, orientation='h')
            st.plotly_chart(fig2, use_container_width=True)

        with tab_graf3:
            st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <h6 style="text-align: center;">Ultimo gasto Mãe</h6>
            </div>
            """, unsafe_allow_html=True
            )
            st.write('Gráfico 3')
            
                       
    st.subheader('Tabelas', divider='blue')

    with st.container():

        tab_dataf1, tab_dataf2, tab_dataf3 = st.columns(3)


        with tab_dataf1:
            st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <h6 style="text-align: center;">Tabela de gastos Mikael</h6>
            </div>
            """, unsafe_allow_html=True
        )
            st.dataframe(data_mika.sort_values(by='data', ascending=False), use_container_width=True, height=900, hide_index=True)
        
        with tab_dataf2:
            st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <h6 style="text-align: center;">Tabela de gastos Mãe</h6>
            </div>
            """, unsafe_allow_html=True
        )
            st.dataframe(data_mae.sort_values(by='data', ascending=False), use_container_width=True, height=900, hide_index=True)
        
        with tab_dataf3:
            st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <h6 style="text-align: center;">Tabela de saldos</h6>
            </div>
            """, unsafe_allow_html=True
        )
            st.dataframe(data_saldo, use_container_width=True, height=900, hide_index=True)

        if st.button('Carregar dados da planilha'):
            data = conn.read_sheet(service, 'gastosmae')
            st.write("Dados da planilha:", data)

        st.subheader("Inserir novos dados")
        nome = st.text_input("Nome")
        idade = st.number_input("Idade", min_value=1, max_value=120, step=1)

        if st.button("Salvar dados"):
            if nome and idade:
                new_data = [nome, str(idade)]  # Ajuste para uma lista simples
                conn.append_data(service, new_data, 'gastosmae')  # Passar a nova linha para a função
                st.success("Dados salvos com sucesso!")

if __name__ == '__main__':
    main()
