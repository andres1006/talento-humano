import React, { useState, useEffect } from "react";
import { apiRequest, Cliente } from "../api/services";

const Clientes: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [clienteActual, setClienteActual] = useState<Cliente>({
    nombre: "",
    email: "",
    telefono: "",
    direccion: "",
    activo: true,
  });
  const [modo, setModo] = useState<"lista" | "crear" | "editar">("lista");
  const [filtro, setFiltro] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    cargarClientes();
  }, []);

  const cargarClientes = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiRequest<Cliente[]>("GET", "/clientes");
      setClientes(response || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar clientes");
      console.error("Error cargando clientes:", err);
    } finally {
      setLoading(false);
    }
  };

  const limpiarFormulario = () => {
    setClienteActual({
      nombre: "",
      email: "",
      telefono: "",
      direccion: "",
      activo: true,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError(null);

      if (modo === "crear") {
        const response = await apiRequest<Cliente>(
          "POST",
          "/clientes",
          clienteActual
        );
        setClientes([...clientes, response]);
      } else if (modo === "editar" && clienteActual.id) {
        const response = await apiRequest<Cliente>(
          "PUT",
          `/clientes/${clienteActual.id}`,
          clienteActual
        );
        setClientes(
          clientes.map((c) => (c.id === clienteActual.id ? response : c))
        );
      }

      setModo("lista");
      limpiarFormulario();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al guardar cliente");
      console.error("Error guardando cliente:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditar = (cliente: Cliente) => {
    setClienteActual(cliente);
    setModo("editar");
  };

  const handleInhabilitar = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await apiRequest("PATCH", `/clientes/${id}/toggle-status`);
      setClientes(
        clientes.map((c) => (c.id === id ? { ...c, activo: !c.activo } : c))
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Error al cambiar estado del cliente"
      );
      console.error("Error cambiando estado:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEliminar = async (id: number) => {
    if (window.confirm("¿Está seguro de que desea eliminar este cliente?")) {
      try {
        setLoading(true);
        setError(null);
        await apiRequest("DELETE", `/clientes/${id}`);
        setClientes(clientes.filter((c) => c.id !== id));
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Error al eliminar cliente"
        );
        console.error("Error eliminando cliente:", err);
      } finally {
        setLoading(false);
      }
    }
  };

  const clientesFiltrados = clientes.filter(
    (cliente) =>
      cliente.nombre.toLowerCase().includes(filtro.toLowerCase()) ||
      cliente.email.toLowerCase().includes(filtro.toLowerCase())
  );

  if (loading && clientes.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Cargando clientes...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">
          Gestión de Clientes
        </h1>
        <button
          onClick={() => {
            setModo("crear");
            limpiarFormulario();
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          disabled={loading}
        >
          Nuevo Cliente
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {modo === "lista" && (
        <div className="space-y-4">
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Buscar clientes..."
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nombre
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Teléfono
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
                {clientesFiltrados.map((cliente) => (
                  <tr key={cliente.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {cliente.nombre}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {cliente.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {cliente.telefono}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          cliente.activo
                            ? "bg-green-100 text-green-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {cliente.activo ? "Activo" : "Inactivo"}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button
                        onClick={() => handleEditar(cliente)}
                        className="text-blue-600 hover:text-blue-900"
                        disabled={loading}
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleInhabilitar(cliente.id!)}
                        className={`${
                          cliente.activo
                            ? "text-red-600 hover:text-red-900"
                            : "text-green-600 hover:text-green-900"
                        }`}
                        disabled={loading}
                      >
                        {cliente.activo ? "Inhabilitar" : "Habilitar"}
                      </button>
                      <button
                        onClick={() => handleEliminar(cliente.id!)}
                        className="text-red-600 hover:text-red-900"
                        disabled={loading}
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
            {modo === "crear" ? "Crear Nuevo Cliente" : "Editar Cliente"}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre de la Empresa
                </label>
                <input
                  type="text"
                  value={clienteActual.nombre}
                  onChange={(e) =>
                    setClienteActual({
                      ...clienteActual,
                      nombre: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={clienteActual.email}
                  onChange={(e) =>
                    setClienteActual({
                      ...clienteActual,
                      email: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Teléfono
                </label>
                <input
                  type="tel"
                  value={clienteActual.telefono}
                  onChange={(e) =>
                    setClienteActual({
                      ...clienteActual,
                      telefono: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Dirección
                </label>
                <input
                  type="text"
                  value={clienteActual.direccion}
                  onChange={(e) =>
                    setClienteActual({
                      ...clienteActual,
                      direccion: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="activo"
                checked={clienteActual.activo}
                onChange={(e) =>
                  setClienteActual({
                    ...clienteActual,
                    activo: e.target.checked,
                  })
                }
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                disabled={loading}
              />
              <label
                htmlFor="activo"
                className="ml-2 block text-sm text-gray-900"
              >
                Cliente Activo
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
                disabled={loading}
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                disabled={loading}
              >
                {loading
                  ? "Guardando..."
                  : modo === "crear"
                  ? "Crear Cliente"
                  : "Actualizar Cliente"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default Clientes;
