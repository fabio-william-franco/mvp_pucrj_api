from sqlalchemy.orm import Session
from model import Custo, Atribuicao
from scipy.optimize import linear_sum_assignment
import pandas as pd

def process_assignments(session: Session):
    """
    Resolve o problema de atribuição e salva os resultados na tabela 'atribuicao'.
    """
   
    custos = session.query(Custo).all()
    
    
    data = [
        {
            "custo_id": c.id,  
            "trabalhador_id": c.trabalhador_id,
            "tarefa_id": c.tarefa_id,
            "custo": c.custo
        }
        for c in custos
    ]
    data_df = pd.DataFrame(data)
    
   
    cost_matrix_df = data_df.pivot(index='trabalhador_id', columns='tarefa_id', values='custo').fillna(1e6)
    cost_matrix = cost_matrix_df.values
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    
    for trabalhador_idx, tarefa_idx in zip(row_ind, col_ind):
        
        custo = data_df[(data_df['trabalhador_id'] == cost_matrix_df.index[trabalhador_idx]) &
                        (data_df['tarefa_id'] == cost_matrix_df.columns[tarefa_idx])]
        if not custo.empty:
            atribuicao = Atribuicao(
                custo_id=custo.iloc[0]['custo_id']
            )
            session.add(atribuicao)
    session.commit()