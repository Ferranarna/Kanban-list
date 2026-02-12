import type { Project, ProjectCreate } from '../types';

const BASE_URL = 'http://127.0.0.1:8000';

// Función para obtener todos los proyectos
export const getProjects = async (): Promise<Project[]> => {
  const response = await fetch(`${BASE_URL}/projects/`);
  
  // Fetch no lanza error en códigos 400 o 500, hay que checkearlo:
  if (!response.ok) {
    throw new Error('Error al obtener los proyectos');
  }

  return await response.json(); // Convertimos la respuesta cruda a JSON
};

// Función para crear un proyecto nuevo
export const createProject = async (project: ProjectCreate): Promise<Project> => {
  const response = await fetch(`${BASE_URL}/projects/`, {
    method: 'POST', // Especificamos el método
    headers: {
      'Content-Type': 'application/json', // Le decimos al servidor que enviamos JSON
    },
    body: JSON.stringify(project), // Convertimos nuestro objeto TS a un string de texto
  });

  if (!response.ok) {
    throw new Error('Error al crear el proyecto');
  }

  return await response.json();
};