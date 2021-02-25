<!-- Generate specifications from table (CSV, Excel) -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/JLoDoesIt/specification-latex">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Generate Specification from Table (CSV, Excel)</h3>

  <p align="center">
    Stop writing documents from scratch when you already did the structuration work under a table format.
    <br />
    <a href="https://github.com/JLoDoesIt/specification-latex"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/JLoDoesIt/specification-latex/issues">Report Bug</a>
    ·
    <a href="https://github.com/JLoDoesIt/specification-latex/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

I have often been involved in design thinking and specification process. Coming out with a feature list is pretty much a mandatory step.
Still taking hours to write and maintain a specification is not something you can afford.
This tool is made for you.
You can very easily generate specification documents by just telling what are your sections and subsections.

### Built With

* [Pandas](https://pandas.pydata.org/)
* [PyLatex](https://github.com/JelteF/PyLaTeX)


### Prerequisites

You should have a running OS with Python3 installed as well as pip3 and virtualenv
For instance on Ubuntu
```sh
sudo apt update
sudo apt install python3 python3-pip virtualenv
```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/JLoDoesIt/specification-latex.git
   cd specification-latex
   ```
2. Create your virtual environment
   ```sh
   virtualenv -p python3 venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
You're done !


<!-- USAGE EXAMPLES -->
## Usage

Just run the main program
```sh
source venv/bin/activate
python main.py
```
Files will be generated in the main folder


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/JLoDoesIt/specification-latex/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Your Name - [@JLo_IT](https://twitter.com/JLo_IT)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Best README Template](https://github.com/othneildrew/Best-README-Template)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/JLoDoesIt/specification-latex.svg?style=for-the-badge
[contributors-url]: https://github.com/JLoDoesIt/specification-latex/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/JLoDoesIt/specification-latex.svg?style=for-the-badge
[forks-url]: https://github.com/JLoDoesIt/specification-latex/network/members
[stars-shield]: https://img.shields.io/github/stars/JLoDoesIt/specification-latex.svg?style=for-the-badge
[stars-url]: https://github.com/JLoDoesIt/specification-latex/stargazers
[issues-shield]: https://img.shields.io/github/issues/JLoDoesIt/specification-latex.svg?style=for-the-badge
[issues-url]: https://github.com/JLoDoesIt/specification-latex/issues
[license-shield]: https://img.shields.io/github/license/JLoDoesIt/specification-latex.svg?style=for-the-badge
[license-url]: https://github.com/JLoDoesIt/specification-latex/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jeanloic-cavazza/
[product-screenshot]: images/screenshot.png

