
export interface ProjectCreate {
  name: string;
  description: string;
}

export interface Project extends ProjectCreate {
  id: number;
  created_at?: string; 
}