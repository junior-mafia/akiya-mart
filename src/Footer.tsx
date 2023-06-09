import React, { useState } from "react"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import { createHash } from "crypto"

const secret =
  "be44c83ac5041f3ac351e6e6b5f1609c7b9287116874d8ae3dbaa279376f387b"
const adminSecret =
  "fb936bdf2d61aa2795770ba1f006cfe088d05d601c126ef616fe61a9cb6d0ea2"

function hashSHA256(value: string): string {
  const hash = createHash("sha256")
  hash.update(value)
  return hash.digest("hex")
}

interface FooterProps {
  setIsPaidTier: (isPaidTier: boolean) => void
  isPaidTier: boolean
}

const Footer = ({ setIsPaidTier, isPaidTier }: FooterProps) => {
  const [inputValue, setInputValue] = useState("")

  const handleButtonClick = () => {
    if (
      hashSHA256(inputValue) === secret ||
      hashSHA256(inputValue) === adminSecret
    ) {
      setIsPaidTier(true)
    } else {
      setIsPaidTier(false)
    }
  }

  const handlePasswordInputChange = (e) => {
    setInputValue(e.target.value)
  }

  return (
    <>
      {!isPaidTier && (
        <div className="footer-container">
          <>
            <div className="footer-subscribe-container">
              <div className="footer-subscribe-message">
                Subscribe to the AkiyaMart newsletter to unlock over 100k
                listings!
              </div>
              <Button
                className="footer-subscribe-button"
                variant="contained"
                color="primary"
                onClick={() =>
                  window.open("https://akiyamart.substack.com/", "_blank")
                }
                sx={{
                  backgroundColor: "#ffabeb",
                  fontFamily: "YuseiMagic",
                  fontSize: "1.0rem",
                  color: "#ffffff",
                  textTransform: "none",
                  "&:hover": {
                    backgroundColor: "#fc80de",
                  },
                }}
              >
                Subscribe
              </Button>
            </div>

            <div className="footer-unlock-container">
              <div className="footer-unlock-message">Already a subscriber?</div>

              <div className="footer-unlock-input-container">
                <TextField
                  label="Password"
                  variant="outlined"
                  value={inputValue}
                  className="footer-unlock-input"
                  onChange={handlePasswordInputChange}
                  InputLabelProps={{
                    sx: { fontFamily: "YuseiMagic", fontSize: "1.0rem" },
                  }}
                  sx={{
                    "& .MuiOutlinedInput-root": {
                      "& fieldset": {
                        borderColor: "#dcdbdc", // Change the border color here
                      },
                      "&:hover fieldset": {
                        borderColor: "#dcdbdc", // Change the border color when hovered here
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "#dcdbdc", // Change the border color when focused here
                      },
                    },
                    "& .MuiInputBase-input": {
                      color: "#dcdbdc", // Change the text color here
                    },
                    "& .MuiFormLabel-root": {
                      color: "#dcdbdc", // Change the label color here
                    },
                    "& .MuiFormLabel-root.Mui-focused": {
                      color: "#dcdbdc", // Change the label color when focused here
                    },
                  }}
                />
                <Button
                  onClick={handleButtonClick}
                  variant="contained"
                  color="primary"
                  className="footer-unlock-button"
                  sx={{
                    backgroundColor: "#ffabeb",
                    fontFamily: "YuseiMagic",
                    fontSize: "1.0rem",
                    color: "#ffffff",
                    textTransform: "none",
                    "&:hover": {
                      backgroundColor: "#fc80de",
                    },
                  }}
                >
                  Unlock
                </Button>
              </div>
            </div>
          </>
        </div>
      )}
    </>
  )
}

export default Footer
