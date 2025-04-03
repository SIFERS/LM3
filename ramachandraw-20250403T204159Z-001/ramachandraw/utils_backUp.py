from functools import wraps
from importlib import resources
from itertools import cycle
from typing import Union
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from Bio.PDB import PDBList
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from ramachandraw.parser import get_phi_psi
import math


class NoPdbIdProvided(Exception):
    pass

def handle_multiple_ids(func):
    """Decorator allowing more than one PDB id to be processed."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        pdbs = None
        if args:
            pdbs = args[0] if args[0] else None
        elif kwargs and not pdbs:
            pdbs = kwargs.get("pdb_id", None)

        verbose = kwargs.get("verbose", False)

        if not pdbs:
            raise NoPdbIdProvided(
                "Please provide one or more PDB ids using the `pdb_id` argument."
            )

        if isinstance(pdbs, str):
            return func(pdb_id=pdbs, verbose=verbose)
        elif isinstance(pdbs, (list, tuple)):
            return [func(pdb_id=pdb, verbose=verbose) for pdb in pdbs]

    return wrapper

@handle_multiple_ids
def fetch_pdb(
    pdb_id: Union[str, list, tuple], verbose: bool = False
) -> Union[str, list[str]]:
    """Fetch PDB file given a PDB id (in .ent format)."""
    pdbl = PDBList(verbose=verbose)
    return pdbl.retrieve_pdb_file(pdb_code=pdb_id, pdir=".pdb", file_format="pdb")

def plot(
    pdb_filepath: Union[str, list, tuple],
    cmap: str = "viridis",
    alpha: float = 0.95,
    dpi: int = 200,
    save: bool = True,
    show: bool = False,
    filename: str = "plot.png",
    density_threshold: float = 1e-08,  # Definir un umbral de densidad para límites permitidos
) -> Axes:
    """Draw the Ramachandrawn plot."""
    
    def plot_density_map() -> None:
        """Plot the density map of allowed/favoured regions."""
        density_file = resources.files(package="ramachandraw") / "kde.dat"
        with density_file.open("r") as kde_data:
            z = np.fromfile(kde_data)
        z = np.reshape(z, (100, 100))

        # Normalize
        data = np.log10(np.rot90(z))
        ax.imshow(
            data, cmap=plt.get_cmap(cmap), extent=(-180, 180, -180, 180), alpha=alpha
        )
        niveles = [10**i for i in range(-9, 1)]
        # Add contour lines
        data = np.rot90(np.fliplr(z))
        contour = ax.contour(
            data,
            colors="k",
            linewidths=0.5,
            levels=niveles,
            antialiased=True,
            extent=[-180, 180, -180, 180],
            alpha=0.5,
        )
        print(data)
        return data, contour


    def draw(contour, data: dict[str, list], color: str = "k") -> None:
        # Iterar sobre cada residuo y sus ángulos de torsión
        for residue, (phi, psi) in data.items():
            # Obtener la densidad correspondiente a (phi, psi)
            density_value = data_density[int((phi + 180) / 360 * 100)][int((psi + 180) / 360 * 100)]
             
            # Inicializar bandera de verificación de si el punto está en el contorno deseado
            dentro_de_contorno = False

            # Revisar cada contorno para ver si coincide con la magnitud deseada
            for i, collection in enumerate(contour.collections):
                # Verificar si el nivel del contorno coincide con el nivel deseado
                if math.log10(contour.levels[i]) == -6:
                    # Revisar cada área del contorno
                    for path in collection.get_paths():
                        # Verificar si el punto (phi, psi) está dentro del contorno
                        if path.contains_point((phi, psi)):
                            dentro_de_contorno = True
                            break
                # Si encontramos que está dentro, salimos del bucle
                if dentro_de_contorno:
                    break

            # Graficar el punto si está dentro del contorno de magnitud deseada
            if dentro_de_contorno:
                pass
            else:
                ax.scatter(phi, psi, marker="o", s=1, color=color)

            

    fig = plt.figure(figsize=(5.5, 5), dpi=dpi)
    ax = plt.subplot(111)

    data_density,contours = plot_density_map()

    ticks = list(range(-180, 181, 45))
    ax.set(
        aspect="equal",
        xlabel="\u03C6",
        ylabel="\u03C8",
        xlim=(-180, 180),
        ylim=(-180, 180),
        xticks=ticks,
        yticks=ticks,
        title=pdb_filepath,
    )
    plt.axhline(y=0, color="k", lw=0.5)
    plt.axvline(x=0, color="k", lw=0.5)
    plt.grid(visible=None, which="major", axis="both", color="k", alpha=0.2)

    angles = get_phi_psi(pdb_filepath=pdb_filepath)

    # Single PDB
    if isinstance(angles, dict):
        draw(contours,data=angles)

    # Multiple PDBs
    elif isinstance(angles, list):
        ax.set_title(f"Batch ({len(pdb_filepath)} files)")
        colors = cycle(mcolors.TABLEAU_COLORS.values())
        custom_legend = []
        for pdb, data in zip(pdb_filepath, angles):
            color = next(colors)
            draw(data=data, color=color)  # type: ignore
            point = Line2D(
                [0],
                [0],
                label=pdb,
                marker="o",
                markerfacecolor=color,
                markeredgewidth=0,
                markersize=5,
                linestyle="",
            )
            custom_legend.append(point)
        handles, _ = plt.gca().get_legend_handles_labels()
        handles.extend(custom_legend)
        ax.legend(handles=handles, loc=1)

    if save:
        fig.savefig(filename)
    if show:
        plt.show()

    return ax, data_density
