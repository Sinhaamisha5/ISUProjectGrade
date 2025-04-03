import { useState } from "react";

export default function GradeLookup() {
    const [selectedCountry, setSelectedCountry] = useState(null);
    const [university, setUniversity] = useState("");
    const [grade, setGrade] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const apiEndpoints = {
        ghana: "http://170.9.243.127:5000/get_grade_point",
        china: "http://170.9.243.127:5000/get_China_grade_point",
        nigeria: "http://170.9.243.127:5000/get_Nigeria_grade_point",
        india: "http://170.9.243.127:5000/get_India_grade_point",
    };

    const fetchGradePoint = async () => {
        if (!selectedCountry || !university || !grade) {
            alert("Please select a country and enter both university and grade");
            return;
        }

        setLoading(true);
        try {
            const encodedGrade = encodeURIComponent(grade);
            const response = await fetch(
                `${apiEndpoints[selectedCountry]}?university=${university}&grade=${encodedGrade}`
            );

            const data = await response.json();
            if (response.ok) {
                setResult(data);
            } else {
                alert(data.error || "Failed to fetch data");
                setResult(null);
            }
        } catch (error) {
            alert("Error fetching data");
        }
        setLoading(false);
    };

    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            height: "100vh",
            backgroundColor: "#f4f4f4",
            fontFamily: "Arial, sans-serif"
        }}>
            <h2>Select a Country</h2>
            <div>
                {Object.keys(apiEndpoints).map((country) => (
                    <button
                        key={country}
                        onClick={() => {
                            setSelectedCountry(country);
                            setResult(null);
                            setUniversity("");
                            setGrade("");
                        }}
                        style={{
                            margin: "5px",
                            padding: "10px",
                            borderRadius: "5px",
                            border: "none",
                            backgroundColor: selectedCountry === country ? "#007BFF" : "#ccc",
                            color: "white",
                            fontWeight: "bold",
                            cursor: "pointer",
                            transition: "background 0.3s"
                        }}
                    >
                        {country.toUpperCase()}
                    </button>
                ))}
            </div>

            {selectedCountry && (
                <div style={{
                    marginTop: "20px",
                    padding: "20px",
                    border: "1px solid black",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    background: "#f9f9f9",
                    borderRadius: "8px",
                    width: "350px"
                }}>
                    <h3>Grade Lookup for {selectedCountry.toUpperCase()}</h3>
                    <div style={{ marginBottom: "10px", width: "100%" }}>
                        <label>University: </label>
                        <input
                            type="text"
                            placeholder="Enter university Name"
                            value={university}
                            onChange={(e) => setUniversity(e.target.value)}
                            style={{ width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
                        />
                    </div>
                    <div style={{ marginBottom: "10px", width: "100%" }}>
                        <label>Grade: </label>
                        <input
                            type="text"
                            placeholder="Enter grade (e.g., A, 75)"
                            value={grade}
                            onChange={(e) => setGrade(e.target.value)}
                            style={{ width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
                        />
                    </div>
                    <button
                        onClick={fetchGradePoint}
                        disabled={loading}
                        style={{
                            width: "100%",
                            padding: "10px",
                            borderRadius: "5px",
                            border: "none",
                            backgroundColor: "#28a745",
                            color: "white",
                            fontWeight: "bold",
                            cursor: "pointer",
                            transition: "background 0.3s"
                        }}
                    >
                        {loading ? "Fetching..." : "Get Equivalent Score"}
                    </button>

                    {result && (
                        <div style={{
                            background: "#fff",
                            padding: "20px",
                            borderRadius: "8px",
                            boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
                            width: "100%",
                            marginTop: "20px",
                            textAlign: "center"
                        }}>
                            <h3>Result</h3>
                            <p><strong>University:</strong> {result.university}</p>
                            <p><strong>Grade:</strong> {result.grade}</p>
                            <p><strong>Format:</strong> {result.format}</p>
                            {result.us_equivalent_scores && (
                                <p><strong>US Equivalent Scores:</strong> {result.us_equivalent_scores.join(", ")}</p>
                            )}
                            {result.closest_grade_matches && (
                                <div style={{ marginTop: "10px" }}>
                                    <p><strong>Closest Grade Matches:</strong></p>
                                    <ul style={{ listStyle: "none", padding: 0 }}>
                                        {result.closest_grade_matches.map((match, idx) => (
                                            <li key={idx}>
                                                Grade: <strong>{match.grade}</strong> → US Score: <strong>{match.us_score}</strong>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

