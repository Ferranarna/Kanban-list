import { useEffect, useState } from 'react';
import { getProjects } from './api/client'; // Importamos nuestro "mensajero"
import type { Project } from './types'; // Importamos el molde de datos

function App() {
  // 1. Creamos el almacén. Empezamos con un array vacío []
  const [projects, setProjects] = useState<Project[]>([]);
  // Un almacén extra para saber si estamos cargando datos
  const [loading, setLoading] = useState<boolean>(true);

  // 2. El disparador: Se ejecuta una sola vez al cargar la web
  useEffect(() => {
    // Llamamos a la función de nuestro client.ts
    getProjects()
      .then((data) => {
        setProjects(data); // Guardamos los datos en el almacén
        setLoading(false); // Ya no estamos cargando
      })
      .catch((error) => {
        console.error("Error cargando proyectos:", error);
        setLoading(false);
      });
  }, []); // Este [] al final significa: "solo hazlo una vez al arrancar"

  // 3. La parte visual (JSX)
  return (
    <div className="p-8 font-sans">
      <h1 className="text-2xl font-bold mb-6">Mis Proyectos Kanban</h1>

      {loading ? (
        <p>Cargando proyectos desde la API...</p>
      ) : (
        <div className="grid gap-4">
          {projects.length === 0 ? (
            <p>No hay proyectos creados todavía.</p>
          ) : (
            projects.map((project) => (
              <div key={project.id} className="p-4 border rounded shadow-sm bg-white">
                <h2 className="font-semibold text-lg">{project.name}</h2>
                <p className="text-gray-600">{project.description}</p>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default App;