import {
  Box,
  HStack,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  Text,
  VStack,
  Select,
  Radio,
  RadioGroup,
  Stack,
  Button,
} from "@chakra-ui/react";
import axios from "axios";
import { useState } from "react";

function App() {
  const [gender, setGender] = useState("Male");
  const [sclass, setSclass] = useState(0);
  const [tclass, setTclass] = useState(0);
  const [age, setAge] = useState(0);
  // const [prediction, setPrediction] = useState(null);
  const [status, setStatus] = useState<string>("");

  const handleAgeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (e.target.value == "1st") {
      setSclass(0);
      setTclass(0);
    } else if (e.target.value == "2nd") {
      setSclass(1);
      setTclass(0);
    } else {
      setSclass(0);
      setTclass(1);
    }
  };

  const handleSubmit = () => {
    let isMale = gender === "Male" ? 1 : 0;

    let reqBody = {
      Age: age,
      PClass_2nd: sclass,
      PClass_3rd: tclass,
      Sex_male: isMale,
    };

    axios
      .post("http://127.0.0.1:5001/predict", reqBody)
      .then((res) => {
        // setPrediction(res.data.prediction);
        if (res.data.prediction === 0) setStatus("Died");
        else setStatus("Survived");
        console.log(res.data.prediction);
      })
      .catch((err) => console.log(err));
  };

  return (
    <Box>
      <Text
        fontSize={"2.5rem"}
        fontWeight={900}
        textAlign={"center"}
        marginTop={"3%"}
      >
        Titanic Survivors Predictions
      </Text>

      <HStack display={"flex"} justifyContent={"space-evenly"}>
        <VStack marginTop={"5%"}>
          <Text fontSize={"1.5rem"} fontWeight={900}>
            Age
          </Text>
          <NumberInput min={0} max={150} onChange={(v) => setAge(parseInt(v))}>
            <NumberInputField required />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </VStack>

        <VStack marginTop={"5%"}>
          <Text fontSize={"1.5rem"} fontWeight={900}>
            Passenger Class
          </Text>
          <Select
            placeholder="Select option"
            required
            onChange={(e) => handleAgeChange(e)}
          >
            <option value="1st">1st Class</option>
            <option value="2nd">2nd Class</option>
            <option value="3rd">3rd Class</option>
          </Select>
        </VStack>

        <VStack marginTop={"5%"}>
          <Text fontSize={"1.5rem"} fontWeight={900}>
            Gender
          </Text>
          <RadioGroup onChange={setGender} value={gender}>
            <Stack direction="row">
              <Radio value="Male">Male</Radio>
              <Radio value="Female">Female</Radio>
            </Stack>
          </RadioGroup>
        </VStack>
      </HStack>

      <HStack display={"flex"} justifyContent={"center"} marginTop={"5%"}>
        <Button width={"30%"} onClick={handleSubmit} fontSize={"1.5rem"}>
          Get Result
        </Button>
      </HStack>

      <HStack display={"flex"} justifyContent={"center"} marginTop={"5%"}>
        <Text
          fontSize={"2rem"}
          fontWeight={500}
          color={status === "Died" ? "red" : "green"}
        >
          {status && status}
        </Text>
      </HStack>
    </Box>
  );
}

export default App;
