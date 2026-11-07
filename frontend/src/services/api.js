const API_URL = "http://127.0.0.1:8000";

export const sendMessageToBackend = async (message) => {
  try {
    const response = await fetch(`${API_URL}/api/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Erro na comunicação com o servidor.");
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Erro:", error);
    return "Desculpa, ocorreu um erro ao contactar o servidor do backend.";
  }
};