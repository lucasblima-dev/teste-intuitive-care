export interface PaginationMeta {
  total: number;
  page: number;
  limit: number;
}

export interface Operadora {
  reg_ans: number;
  razao_social: string | null;
  uf: string | null;
}

export interface OperadorasResponse extends PaginationMeta {
  data: Operadora[];
}

export interface Despesa {
  descricao_conta: string;
  ano: number;
  trimestre: string;
  valor: number;
}

export interface StatsUF {
  uf: string;
  total_despesas: number;
}