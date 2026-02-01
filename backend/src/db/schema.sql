CREATE TABLE IF NOT EXISTS operadoras (
    reg_ans INT PRIMARY KEY,
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf VARCHAR(2)
);

CREATE TABLE IF NOT EXISTS despesas (
    id SERIAL PRIMARY KEY,
    reg_ans INT NOT NULL,
    descricao_conta VARCHAR(255),
    data_evento DATE,
    trimestre VARCHAR(2),
    ano INT,
    valor DECIMAL(15,2),
    CONSTRAINT fk_operadora
        FOREIGN KEY (reg_ans)
        REFERENCES operadoras(reg_ans)
);

CREATE INDEX idx_despesas_reg_ans ON despesas(reg_ans);
CREATE INDEX idx_despesas_ano_trimestre ON despesas(ano, trimestre);