-- As 5 operadoras com maior despesa total no último trimestre
SELECT 
    o.reg_ans,
    o.razao_social,
    SUM(d.valor) as total_despesas
FROM operadoras o
JOIN despesas d ON o.reg_ans = d.reg_ans
WHERE d.ano = 2025 AND d.trimestre = '3T'
GROUP BY o.reg_ans, o.razao_social
ORDER BY total_despesas DESC
LIMIT 5;

-- Despesas por estados (os 5 princiapis )
SELECT 
    o.uf,
    SUM(d.valor) as total_despesas,
    AVG(d.valor) as media_por_lancamento
FROM operadoras o
JOIN despesas d ON o.reg_ans = d.reg_ans
WHERE o.uf IS NOT NULL
GROUP BY o.uf
ORDER BY total_despesas DESC
LIMIT 5;

-- Despesas acima da média geral
WITH MediaGeral AS (
    SELECT AVG(valor) as media_valor FROM despesas
)
SELECT 
    o.reg_ans, 
    o.razao_social,
    COUNT(d.id) as qtd_lancamentos_acima_media
FROM operadoras o
JOIN despesas d ON o.reg_ans = d.reg_ans
CROSS JOIN MediaGeral mg
WHERE d.valor > mg.media_valor
GROUP BY o.reg_ans, o.razao_social
ORDER BY qtd_lancamentos_acima_media DESC
LIMIT 10;