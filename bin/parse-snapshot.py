#!/usr/bin/env python3

<<<<<<< HEAD
import os
from typing import Any, MutableMapping

from pydantic import BaseModel, ConfigDict, AnyUrl, Field, model_validator


class Git(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: AnyUrl
    revision: str


class Source(BaseModel):
    model_config = ConfigDict(frozen=True)

    git: Git


class ContainerImage(BaseModel):
    model_config = ConfigDict(frozen=True)

    image: str
    sha: str


class Component(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    container_image: ContainerImage = Field(alias="containerImage")
    source: Source

    @model_validator(mode='before')
    @classmethod
    def container_image_validator(cls, data: Any) -> Any:
        if not isinstance(data, MutableMapping):
            raise ValueError(f"{data} is not of mapping type")

        image, sha = data["containerImage"].split("@sha256:")
        data["containerImage"] = ContainerImage(image=image, sha=sha)
        return data


class Snapshot(BaseModel):
    model_config = ConfigDict(frozen=True)

    application: str
    components: list[Component]
=======
import json
import os
from typing import Mapping
from textwrap import dedent
>>>>>>> 596c3c7 (Build image for RHTAP pipelines)


def main() -> None:
    snapshot_str = os.environ.get("SNAPSHOT")
    if snapshot_str is None:
        raise RuntimeError("SNAPSHOT environment variable wasn't declared or empty")
<<<<<<< HEAD
    snapshot: Snapshot = Snapshot.model_validate_json(snapshot_str)
    ret = []
    for component in snapshot.components:
        component_name = os.environ.get("BONFIRE_COMPONENT_NAME", component.name)
        ret.extend((
            "--set-template-ref",
            f"{component_name}={component.source.git.revision}",
            "--set-parameter",
            f"{component_name}/IMAGE={component.container_image.image}@sha256",
            "--set-parameter",
            f"{component_name}/IMAGE_TAG={component.container_image.sha}"
        ))
    print(" ".join(ret))
=======
    snapshot: Mapping = json.loads(snapshot_str)
    components = snapshot.get("components")
    if not components:
        raise RuntimeError(f"No components found in SNAPSHOT: ${snapshot}")
    if len(components) > 1:
        raise RuntimeError(
            f"Can't handle snapshot that has more than 1 component. Got SNAPSHOT: ${snapshot}"
        )

    container_image = components[0]["containerImage"].split("@sha256")[0]
    tag = components[0]["source"]["git"]["revision"]

    print(dedent(
        f"""
        export IMAGE={container_image} IMAGE_TAG={tag} GIT_COMMIT={tag}
        """
    ))
>>>>>>> 596c3c7 (Build image for RHTAP pipelines)


if __name__ == "__main__":
    main()
