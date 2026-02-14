import { useEffect, useState } from 'react';
import { getProjects, createProject } from './api/client';
import type { Project, ProjectCreate } from './types';
import { ProjectForm } from './components/ProjectForm';

function App() {
  const [projects, setProjects] = useState<Project[]>([]);

  // 1. Cargar proyectos al inicio
  useEffect(() => {
    getProjects().then(setProjects).catch(console.error);
  }, []);

  // 2. Función para manejar la creación
  const handleCreateProject = async (projectData: ProjectCreate) => {
    try {
      const savedProject = await createProject(projectData);
      // Actualizamos la lista local agregando el nuevo proyecto al final
      setProjects([...projects, savedProject]);
    } catch (error) {
      alert("Error al guardar en el servidor");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-extrabold text-slate-900 mb-8">Gestor Kanban</h1>

        {/* Sección de Proyectos */}
        <section className="mb-12">
          <ProjectForm onProjectCreated={handleCreateProject} />
          
          <div className="grid gap-4">
            {projects.map(project => (
              <div key={project.id} className="bg-white p-4 rounded-lg border border-slate-200 flex justify-between items-center shadow-sm">
                <div>
                  <span className="text-xs font-mono text-slate-400 block">ID: {project.id}</span>
                  <h3 className="font-bold text-slate-800">{project.name}</h3>
                  <p className="text-slate-600 text-sm">{project.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <hr className="my-12 border-slate-200" />

        {/* Aquí irán las secciones de Épicas y Tareas más adelante */}
        <div className="opacity-50 pointer-events-none">
          <h2 className="text-2xl font-bold text-slate-400 mb-4 text-center italic">
            Sección de Épicas (Próximamente...)
          </h2>
        </div>
      </div>
    </div>
  );
}

export default App;