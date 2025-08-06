import React, { useState, useEffect, useCallback } from "react";
import { apiRequest } from "../api/services";
import { CandidatoResponse } from "../types/candidatos.type";
import { CiudadResponse } from "../types/ciudad.type";

const Candidatos: React.FC = () => {
  const [candidatos, setCandidatos] = useState<CandidatoResponse[]>([]);
  const [candidatoActual, setCandidatoActual] = useState<CandidatoResponse>({
    nombre: "",
    apellido: "",
    tipo_documento: "",
    cedula: "",
    fecha_nacimiento: "",
    rh: "",
    ciudad_expedicion_id: 0,
    ciudad_nacimiento_id: 0,
    ciudad_domicilio_id: 0,
    activo: true,
    nombres_ciudades: {
      ciudad_expedicion: "",
      ciudad_nacimiento: "",
      ciudad_domicilio: "",
    },
  });
  const [ciudades, setCiudades] = useState<CiudadResponse[]>([]);
  const [modo, setModo] = useState<"lista" | "crear" | "editar">("lista");
  const [filtro, setFiltro] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    cargarCandidatos();
    cargarCiudades();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const cargarCandidatos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiRequest<CandidatoResponse[]>(
        "GET",
        "/candidatos"
      );
      console.log("🔄 Candidatos:", response);
      setCandidatos(response || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar clientes");
      console.error("Error cargando clientes:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  const cargarCiudades = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiRequest<CiudadResponse[]>("GET", "/ciudades");
      setCiudades(response || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar ciudades");
      console.error("Error cargando ciudades:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  const limpiarFormulario = () => {
    setCandidatoActual({
      nombre: "",
      apellido: "",
      tipo_documento: "",
      cedula: "",
      fecha_nacimiento: "",
      rh: "",
      ciudad_expedicion_id: 0,
      ciudad_nacimiento_id: 0,
      ciudad_domicilio_id: 0,
      activo: true,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (modo === "crear") {
      const nuevoCandidato: CandidatoResponse = {
        ...candidatoActual,
        id: Math.max(...candidatos.map((c) => c.id || 0)) + 1,
      };
      setCandidatos([...candidatos, nuevoCandidato]);
    } else if (modo === "editar") {
      setCandidatos(
        candidatos.map((c) =>
          c.id === candidatoActual.id ? candidatoActual : c
        )
      );
    }

    setModo("lista");
    limpiarFormulario();
  };

  const handleEditar = (candidato: CandidatoResponse) => {
    setCandidatoActual(candidato);
    setModo("editar");
  };

  const handleInhabilitar = async (id: number) => {
    const candidato = candidatos.find((c) => c.id === id);
    if (candidato) {
      delete candidato.nombres_ciudades;

      // Asegurar que la fecha esté en el formato correcto (YYYY-MM-DD)
      const fechaNacimiento = candidato.fecha_nacimiento.split("T")[0];

      const response = await apiRequest<{ message: string }>(
        "PUT",
        `/candidatos/${id}`,
        {
          nombre: candidato.nombre,
          apellido: candidato.apellido,
          tipo_documento: candidato.tipo_documento,
          cedula: candidato.cedula,
          fecha_nacimiento: fechaNacimiento,
          rh: candidato.rh,
          ciudad_expedicion_id: candidato.ciudad_expedicion_id,
          ciudad_nacimiento_id: candidato.ciudad_nacimiento_id,
          ciudad_domicilio_id: candidato.ciudad_domicilio_id,
          activo: !candidato.activo,
        }
      );
      console.log("🔄 Inhabilitar candidato:", response);
      if (response) {
        setCandidatos(
          candidatos.map((c) => (c.id === id ? { ...c, activo: !c.activo } : c))
        );
      }
    }
  };

  const handleEliminar = (id: number) => {
    if (window.confirm("¿Está seguro de que desea eliminar este candidato?")) {
      setCandidatos(candidatos.filter((c) => c.id !== id));
    }
  };

  const candidatosFiltrados = candidatos.filter((candidato) =>
    `${candidato.nombre} ${candidato.apellido}`
      .toLowerCase()
      .includes(filtro.toLowerCase())
  );

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">
          Gestión de Candidatos
        </h1>
        <button
          onClick={() => {
            setModo("crear");
            limpiarFormulario();
          }}
          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
        >
          Nuevo Candidato
        </button>
      </div>

      {modo === "lista" && (
        <div className="space-y-4">
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Buscar candidatos..."
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nombre Completo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Teléfono
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Experiencia
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {candidatosFiltrados.map((candidato) => (
                  <tr key={candidato.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {candidato.nombre} {candidato.apellido}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {candidato.tipo_documento}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {candidato.cedula}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {candidato.fecha_nacimiento}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          candidato.activo
                            ? "bg-green-100 text-green-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {candidato.activo ? "Activo" : "Inactivo"}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button
                        onClick={() => handleEditar(candidato)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleInhabilitar(candidato.id!)}
                        className={`${
                          candidato.activo
                            ? "text-red-600 hover:text-red-900"
                            : "text-green-600 hover:text-green-900"
                        }`}
                      >
                        {candidato.activo ? "Inhabilitar" : "Habilitar"}
                      </button>
                      <button
                        onClick={() => handleEliminar(candidato.id!)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {(modo === "crear" || modo === "editar") && (
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {modo === "crear" ? "Crear Nuevo Candidato" : "Editar Candidato"}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre
                </label>
                <input
                  type="text"
                  value={candidatoActual.nombre}
                  onChange={(e) =>
                    setCandidatoActual({
                      ...candidatoActual,
                      nombre: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Apellido
                </label>
                <input
                  type="text"
                  value={candidatoActual.apellido}
                  onChange={(e) =>
                    setCandidatoActual({
                      ...candidatoActual,
                      apellido: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={candidatoActual.tipo_documento}
                  onChange={(e) =>
                    setCandidatoActual({
                      ...candidatoActual,
                      tipo_documento: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Teléfono
                </label>
                <input
                  type="tel"
                  value={candidatoActual.cedula}
                  onChange={(e) =>
                    setCandidatoActual({
                      ...candidatoActual,
                      cedula: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Experiencia
              </label>
              <textarea
                value={candidatoActual.fecha_nacimiento}
                onChange={(e) =>
                  setCandidatoActual({
                    ...candidatoActual,
                    fecha_nacimiento: e.target.value,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                rows={3}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Habilidades
              </label>
              <textarea
                value={candidatoActual.rh}
                onChange={(e) =>
                  setCandidatoActual({
                    ...candidatoActual,
                    rh: e.target.value,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                rows={3}
                placeholder="Ej: React, Node.js, TypeScript, etc."
                required
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="activo"
                checked={candidatoActual.activo}
                onChange={(e) =>
                  setCandidatoActual({
                    ...candidatoActual,
                    activo: e.target.checked,
                  })
                }
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label
                htmlFor="activo"
                className="ml-2 block text-sm text-gray-900"
              >
                Candidato Activo
              </label>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => {
                  setModo("lista");
                  limpiarFormulario();
                }}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                {modo === "crear" ? "Crear Candidato" : "Actualizar Candidato"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default Candidatos;
