import { useState } from "react";

export default function GradeLookup() {
    const [selectedCountry, setSelectedCountry] = useState(null);
    const [university, setUniversity] = useState("");
    const [grade, setGrade] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [ghanaUniversities, setGhanaUniversities] = useState([]);

    const [selectedState, setSelectedState] = useState("");
    const [selectedCity, setSelectedCity] = useState("");
    const [nigeriaUniversities, setNigeriaUniversities] = useState([]);
    const [chinaUniversities, setChinaUniversities] = useState([]);
    const [indiaUniversities, setIndiaUniversities] = useState([]);



    const [error, setError] = useState(null);


    const apiEndpoints = {
        ghana: "http://localhost:5000/get_grade_point",
        china: "http://localhost:5000/get_China_grade_point",
        nigeria: "http://localhost:5000/get_Nigeria_grade_point",
        india: "http://localhost:5000/get_India_grade_point",
    };

    const fetchUniversityList = async () => {
        try {
            const response = await fetch("http://localhost:5000/get_ghana_universities");
            const data = await response.json();
            setGhanaUniversities(data);
        } catch (error) {
            console.error("Error fetching university list:", error);
        }
    };

    const fetchNigeriaUniversities = async () => {
        try {
            const response = await fetch("http://localhost:5000/get_nigeria_universities");
            const data = await response.json();
            setNigeriaUniversities(data);
        } catch (error) {
            console.error("Error fetching Nigeria universities", error);
        }
    };


    const handleCountrySelect = (country) => {
        setSelectedCountry(country);
        setResult(null);
        setUniversity("");
        setGrade("");
        if (country === "ghana") {
            fetchUniversityList();
        }
        if (country === "india") fetchIndiaMetadata();
        if (country === "nigeria") fetchNigeriaUniversities();
        if (country === "china") {
            const fetchChinaUniversities = async () => {
                try {
                    const response = await fetch("http://localhost:5000/get_china_universities");
                    const data = await response.json();
                    setChinaUniversities(data);
                } catch (error) {
                    console.error("Error fetching China universities", error);
                }
            };
            fetchChinaUniversities();
        }

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
                let message = data.error || "Failed to fetch data";
                if (data.valid_formats) {
                    message += `\nValid formats used by this university: ${data.valid_formats.join(", ")}`;
                }
                alert(message);
                setResult(null);
            }
        } catch (error) {
            setError({ message: "Error fetching data", formats: null });
            setResult(null);
        }
        setLoading(false);
    };

    const fetchIndiaMetadata = async () => {
        try {
            const response = await fetch("http://localhost:5000/get_india_universities");
            const data = await response.json();
            setIndiaUniversities(data); // This now contains [{Display, Name of the University}]
        } catch (error) {
            console.error("Error fetching India metadata:", error);
        }
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
                        onClick={() => handleCountrySelect(country)}
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

                    <div style={{ marginBottom: "10px", textAlign: "right", width: "100%" }}>
                        <a
                            href={`http://localhost:5000/download/${selectedCountry}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                                display: "inline-block",
                                textDecoration: "none",
                                fontSize: "18px",
                                padding: "6px 10px",
                                backgroundColor: "#f0f0f0",
                                borderRadius: "50%",
                                cursor: "pointer",
                                boxShadow: "0 1px 3px rgba(0,0,0,0.2)"
                            }}
                            title={`Download ${selectedCountry.toUpperCase()} Excel`}
                        >
                            📥
                        </a>
                    </div>




                    {/* India-specific cascading dropdowns */}
                    {selectedCountry === "india" ? (
                        <div style={{ marginBottom: "10px", width: "100%" }}>
                            <label>University:</label>
                            <select
                                value={university}
                                onChange={(e) => setUniversity(e.target.value)}
                                style={{ width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
                            >
                                <option value="">Select a university</option>
                                {indiaUniversities.map((item, idx) => (
                                    <option key={idx} value={item["Name of the University"]}>
                                        {item.Display}
                                    </option>
                                ))}
                            </select>
                        </div>
                    ) : (


                        // Ghana and others remain as is
                        <div style={{ marginBottom: "10px", width: "100%" }}>
                            <label>University: </label>
                            {(selectedCountry === "ghana" || selectedCountry === "nigeria" || selectedCountry === "china") ? (
                                <select
                                    value={university}
                                    onChange={(e) => setUniversity(e.target.value)}
                                    style={{ width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
                                >
                                    <option value="">Select a university</option>
                                    {(selectedCountry === "ghana"
                                        ? ghanaUniversities
                                        : selectedCountry === "nigeria"
                                            ? nigeriaUniversities
                                            : chinaUniversities).map((uni, idx) => (
                                                <option key={idx} value={uni}>{uni}</option>
                                            ))}
                                </select>
                            ) : (
                                <input
                                    type="text"
                                    placeholder="Enter university Name"
                                    value={university}
                                    onChange={(e) => setUniversity(e.target.value)}
                                    style={{ width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
                                />
                            )}
                        </div>
                    )}


                    {/* Grade Input */}
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

                    {/* Results */}
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